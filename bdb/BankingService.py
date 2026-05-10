import sqlite3

from sqlite3 import Connection
from time import time
from typing import Optional
from dependencies import database


class BankingService:
    db_connection: Connection = None
    bank_own_account_id = 1
    max_tries = 3

    def __init__(self, db_connection: Optional[Connection]):
        if db_connection is not None:
            self.db_connection = db_connection

        pass

    def get_transactions(self, account_id):
        pass

    def init_data_store(self) -> sqlite3.Connection:
        if self.db_connection is None:
            self.db_connection = database()

        return self.db_connection

    def close_data_store_connection(self):
        self.db_connection.close()

    def validate_user(self, username, password) -> Optional[int]:
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

        rows = cursor.fetchall()

        self.close_data_store_connection()

        if (len(rows)):
            return rows[0]['id']
        else:
            return None

    def get_account(self, account_id):
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
            "INSERT INTO transactions (destination_account, amount, status, balance, kind, tries, timestamp)"
            (bank_account['id'], amount, "COMPLETED", new_current_balance, "FEE", 1, int(time()))
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

            new_destination_current_balance = destination_account['current_balance'] + (transaction['amount'] - fees)
            new_destination_available_balance = destination_account['available_balance'] + (transaction['amount'] - fees)

            cursor.execute("UPDATE accounts SET current_balance=?, available_balance=? WHERE id = ?", (new_destination_current_balance, new_destination_available_balance, transaction['destination_account_id']))

            connection.commit()

            cursor.execute(
                "UPDATE transactions SET status=?, balance=?, tries=? WHERE id=? AND updated_at=?",
                ("COMPLETED", new_destination_current_balance, transaction['tries']+1, transaction['id'], transaction['updated_at'])
            )
            connection.commit()

            results['processed'] += 1

        print("Jobs Processed/Failed: " + str(results['processed']) + "/" + str(results['failed']))

        self.close_data_store_connection()
