import sqlite3

from sqlite3 import Connection
from typing import Optional
from User import User
from Temporal import iso8601, unix_timestamp_s
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
        
        cursor.execute('SELECT * FROM transactions WHERE source_account_id=? OR recipient_account_id=? ORDER BY timestamp DESC', (account_id, account_id))

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

    def get_user_by_id(self, id: int):
        connection = self.init_data_store()

        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id=?', (id,))

        return cursor.fetchone()

    def get_account_by_id(self, id: int):
        connection = self.init_data_store()

        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM accounts WHERE id=?", (id,))

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

    def save_transfer_fee_txn(self, source_account_id: int, amount: int,connection: Optional[sqlite3.Connection] = None):
        connection_passed = False

        if connection is None:
            connection = self.init_data_store()
        else:
            connection_passed = True

        # The bank's account ID is always this ID
        bank_account_id = 1

        cursor = connection.cursor()

        # This should be a pending transaction but for simplicity we keep it COMPLETED. You pay the fee upfront after all.
        cursor.execute(
            """
            INSERT INTO transactions (
                source_account_id,
                recipient_account_id,
                amount,
                fees,
                status,
                kind,
                tries
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (source_account_id, bank_account_id, amount, 0, "PENDING", "FEE", 1)
        )

        connection.commit()

        if cursor.lastrowid > 0:
            print(
                f"[{iso8601()}]: New transaction created",
                {
                    "id": cursor.lastrowid,
                    "source_account_id": source_account_id,
                    "recipient_account_id": id,
                    "amount": amount,
                    "fees": 0,
                    "kind": "FEE",
                    "timestamp": unix_timestamp_s(),
                    "date_time": iso8601()
                }
            )

        # If no connection was passed, it means we created a connection and need to release it.
        # Otherwise, let the caller terminate it themselves
        if connection_passed is False:
            self.close_data_store_connection()

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
            transaction_amount_w_fees = transaction['amount'] + (transaction['fees'] or 0)

            # If this passes, it means that somebody (source_account_id) is trying to send money elsewhere (recipient_account_id)
            # Because all transactions are already debited to begin with from the sender, we only complete the transaction by
            # committing the updates to the recipient and reconciling the balances including the sender
            if transaction['source_account_id'] is not None:
                # Debit the sender first
                source_account = self.get_account(transaction['source_account_id'])

                new_source_account_current_balance = source_account['current_balance'] - transaction_amount_w_fees

                # Set sender current balance
                cursor.execute(
                    "UPDATE accounts SET current_balance=? WHERE id=?",
                    (new_source_account_current_balance, source_account['id'])
                )

                print(
                    f"[{iso8601()}]: Account balance for source account updated",
                    {
                        "account_id": source_account['id'],
                        "from_current_balance": source_account['current_balance'],
                        "from_available_balance": source_account['available_balance'],
                        "to_current_balance": new_source_account_current_balance, # The only value that updated
                        "to_available_balance": source_account['available_balance'],
                    }
                )

            # Now we update the recipient's account

            # Get the recipient account
            recipient_account = self.get_account(transaction['recipient_account_id'])

            amount_without_fees = transaction['amount']

            new_recipient_current_balance = recipient_account['current_balance'] + amount_without_fees
            new_recipient_available_balance = recipient_account['available_balance'] + amount_without_fees

            cursor.execute("UPDATE accounts SET current_balance=?, available_balance=? WHERE id = ?", (new_recipient_current_balance, new_recipient_available_balance, transaction['recipient_account_id']))

            connection.commit()

            print(
                f"[{iso8601()}]: Account balance for recipient account updated",
                {
                    "account_id": transaction['recipient_account_id'],
                    "from_current_balance": recipient_account['current_balance'],
                    "from_available_balance": recipient_account['available_balance'],
                    "to_current_balance": new_recipient_current_balance,
                    "to_available_balance": new_recipient_available_balance
                }
            )

            tries = transaction['tries'] + 1

            cursor.execute(
                "UPDATE transactions SET status=?, tries=? WHERE id=? AND updated_at=?",
                ("COMPLETED", tries, transaction['id'], transaction['updated_at'])
            )

            connection.commit()

            print(
                f"[{iso8601()}]: Transaction completed",
                {
                    "transaction_id": transaction['id'],
                    "updated_at": transaction['updated_at'],
                    "tries": tries,
                }
            )

            results['processed'] += 1

        print("Jobs Processed: " + str(results['processed']))

        self.close_data_store_connection()

    def get_account_transaction_with_id(self, account_id: int, transaction_id: int):
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM transactions WHERE id=? AND recipient_account_id=?", (transaction_id, account_id))

        row = cursor.fetchone()

        self.close_data_store_connection()

        return row

    def get_transaction_with_id(self, id: int, connection: Optional[sqlite3.Connection] = None):
        connection_passed = False

        if connection is None:
            connection = self.init_data_store()
        else:
            connection_passed = True

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM transactions WHERE id=?", (id,))

        transaction_row = cursor.fetchone()

        connection.commit()

        # If no connection was passed, it means we created a connection and need to release it.
        # Otherwise, let the caller terminate it themselves
        if connection_passed is False:
            self.close_data_store_connection()

        return transaction_row

    def update_account_available_balance(self, account_id, amount, connection: Optional[sqlite3.Connection] = None) -> bool:
        result = None
        connection_passed = False

        if connection is None:
            connection = self.init_data_store()
        else:
            connection_passed = True

        account = self.get_account_by_id(account_id)
        new_available_balance = account["available_balance"] + amount

        if new_available_balance < 0:
            result = False
        
        if result is not False:
            cursor = connection.cursor()

            cursor.execute(
                "UPDATE accounts SET available_balance=? WHERE id=?",
                (new_available_balance, account_id)
            )

            connection.commit()

            print(
                f"[{iso8601()}]: Account balance for source account updated",
                {
                    "account_id": account['id'],
                    "from_current_balance": account['current_balance'],
                    "from_available_balance": account['available_balance'],
                    "to_current_balance": account['current_balance'],
                    "to_available_balance": new_available_balance,
                }
            )

            result = True

        # If no connection was passed, it means we created a connection and need to release it.
        # Otherwise, let the caller terminate it themselves
        if connection_passed is False:
            self.close_data_store_connection()

        return result

    def new_transaction(self,
        account_id:int,
        recipient_account_id:int,
        amount:int,
        fees:int,
        message:str
    ):
        connection = self.init_data_store()

        # Update sender balances
        self.update_account_available_balance(account_id, -(amount+fees), connection)

        cursor = connection.cursor()

        cursor.execute("""
            insert into transactions
                (
                    source_account_id,
                    recipient_account_id,
                    amount,
                    message,
                    status,
                    fees,
                    kind
                )
            values
                (?, ?, ?, ?, ?, ?, ?);
        """, (account_id, recipient_account_id, amount, message, "PENDING", fees, "TRANSFER"))

        connection.commit()

        transaction = None

        if cursor.lastrowid is not None:
            transaction = self.get_transaction_with_id(cursor.lastrowid, connection)

            print(
                f"[{iso8601()}]: New transaction created",
                {
                    "id": cursor.lastrowid,
                    "source_account_id": account_id,
                    "recipient_account_id": recipient_account_id,
                    "amount": amount,
                    "fees": fees,
                    "kind": "TRANSFER",
                    "timestamp": unix_timestamp_s(),
                    "date_time": iso8601()
                }
            )

        self.save_transfer_fee_txn(account_id, fees, connection)

        self.close_data_store_connection()

        return transaction
