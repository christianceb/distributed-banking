import sqlite3

from sqlite3 import Connection
from time import time
from typing import Optional
from User import User
from dependencies import database


class BankingService:
    db_connection: Connection = None
    bank_own_account_id = 1
    max_tries = 3

    def __init__(self, db_connection: Optional[Connection]):
        if db_connection is not None:
            self.db_connection = db_connection

    def get_transactions_by_account_id(self, account_id):
        connection = self.init_data_store()

        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM transactions WHERE source_account_id=? OR destination_account_id=? ORDER BY timestamp DESC', (account_id, account_id))

        return cursor.fetchall()

    def init_data_store(self) -> sqlite3.Connection:
        if self.db_connection is None:
            self.db_connection = database()

        return self.db_connection

    def close_data_store_connection(self):
        self.db_connection.close()
        self.db_connection = None

    def get_user_by_username_password(self, username, password) -> Optional[User]:
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

        row = cursor.fetchone()

        self.close_data_store_connection()

        if (row):
            user = User()

            user.id = row['id']
            user.username = row['username']

            return user
        else:
            return None

    def get_user_by_id(self, id):
        connection = self.init_data_store()

        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id=?', (id))

        return cursor.fetchone()

    def get_account_by_user_id(self, user_id):
        connection = self.init_data_store()

        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM accounts WHERE user_id=?', (user_id,))

        return cursor.fetchone()

    def get_account(self, account_id: int):
        connection = self.init_data_store()

        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM accounts WHERE id=?', (account_id,))

        return cursor.fetchone()

    def transfer_fees(self, amount):
        connection = self.init_data_store()

        bank_account = self.get_account(1)

        new_current_balance = bank_account['current_balance']
        new_available_balance = bank_account['available_balance']

        cursor = connection.cursor()

        cursor.execute(
            'UPDATE accounts SET current_balance=?, available_balance=? WHERE id=?',
            (new_current_balance, new_available_balance, bank_account['id'])
        )

        connection.commit()

        # This should be a pending transaction but for simplicity we keep it
        cursor.execute(
            "INSERT INTO transactions (destination_account, amount, status, kind, tries, timestamp)",
            (bank_account['id'], amount, "COMPLETED", "FEE", 1, int(time()))
        )

        connection.commit()

    def process_transactions(self):
        # Reference for future use re: current/available: https://www.bankrate.com/banking/checking/what-is-your-available-balance/
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM transactions WHERE status=? AND tries < ? ORDER BY timestamp", ("PENDING", self.max_tries,))

        rows = cursor.fetchall()

        results = {
            "processed": 0,
            "failed": 0
        }

        for transaction in rows:
            fees = 0 if transaction['fees'] is None else transaction['fees']

            # If this passes, it means that somebody (source_account_id) is trying to send money elsewhere (destination_account_id)
            if transaction['source_account_id'] is not None:
                # Debit the sender first
                source_account = self.get_account(transaction['source_account_id'])

                new_source_account_current_balance = source_account['current_balance'] - transaction['amount']

                if new_source_account_current_balance > 0:
                    cursor.execute(
                        "UPDATE accounts SET current_balance=? WHERE id=?",
                        (new_source_account_current_balance, source_account['id'])
                    )

                    cursor.execute(
                        "UPDATE transactions SET status=?, balance=?, tries=? WHERE id=?",
                        ("COMPLETED", new_source_account_current_balance, transaction['tries'] + 1, transaction['source_account_id'])
                    )

                    connection.commit();
                
                    self.transfer_fees(fees)
                else:
                    cursor.execute(
                        "UPDATE accounts SET available_balance=? WHERE id=?",
                        (source_account['current_balance'], source_account['id'])
                    )

                    cursor.execute(
                        "UPDATE transactions SET status=?, balance=?, tries=? WHERE id=?",
                        ("FAILED", new_source_account_current_balance, transaction['tries'] + 1, transaction['source_account_id'])
                    )

            # Get the destination account
            destination_account = self.get_account(transaction['destination_account_id'])

            amount_without_fees = transaction['amount'] - fees

            new_destination_current_balance = destination_account['current_balance'] + amount_without_fees
            new_destination_available_balance = destination_account['available_balance'] + amount_without_fees

            cursor.execute("UPDATE accounts SET current_balance=?, available_balance=? WHERE id = ?", (new_destination_current_balance, new_destination_available_balance, transaction['destination_account_id']))

            connection.commit()

            print(
                "Account balance for account updated",
                {
                    "account_id": transaction['destination_account_id'],
                    "from_current_balance": destination_account['current_balance'],
                    "from_available_balance": destination_account['available_balance'],
                    "to_current_balance": new_destination_current_balance,
                    "to_available_balance": new_destination_available_balance
                }
            )

            tries = transaction['tries']+1
            cursor.execute(
                "UPDATE transactions SET status=?, tries=? WHERE id=? AND updated_at=?",
                ("COMPLETED", tries, transaction['id'], transaction['updated_at'])
            )
            connection.commit()

            print(
                "Transaction completed",
                {
                    "transaction_id": transaction['id'],
                    "updated_at": transaction['updated_at'],
                    "tries": tries,
                }
            )

            results['processed'] += 1

        print("Jobs Processed/Failed: " + str(results['processed']) + "/" + str(results['failed']))

        self.close_data_store_connection()

    def get_account_transaction_with_id(self, account_id: int, transaction_id: int):
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM transactions WHERE id=? AND account_id=?", (transaction_id, account_id))

        self.close_data_store_connection()

        return cursor.fetchone()

    def get_transaction_with_id(self, id: int, connection: Optional[sqlite3.Connection] = None):
        connection_passed = False

        if connection is None:
            connection = self.init_data_store()
        else:
            connection_passed = False

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM transactions WHERE id=?", (id))

        transaction_row = cursor.fetchone()

        connection.commit()

        if connection_passed is True:
            connection.close()
        else:
            self.close_data_store_connection()

        return transaction_row

    def new_transaction(self,
        account_id:int,
        recipient_account_id:int,
        amount:int,
        fees:int,
        message:str
    ):
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("""
            insert into transactions
                (
                    source_account_id,
                    destination_account_id,
                    amount,
                    status,
                    fees,
                    kind
                )
            values
                (?, ?, ?, ?, ?, ?);
        """, (account_id, recipient_account_id, amount, fees, message))

        connection.commit()

        transaction = None

        if cursor.lastrowid is not None:
            transaction = self.get_transaction_with_id(cursor.lastrowid, connection)

        self.close_data_store_connection()

        return transaction
