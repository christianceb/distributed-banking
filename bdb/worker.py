import sqlite3
import time

from BankingService import BankingService
from dependencies import database
from migrations import clearMigrateSeed

def worker_job(connection: sqlite3.Connection):
    banking_service = BankingService(connection)

    banking_service.process_transactions()

def worker_task():
    try:
        connection = database()

        worker_job(connection)
    except Exception as e:
        raise e
    finally:
        connection.close()

        print("Terminated DB connection")

def worker():
    seconds = 5

    while True:
        try:
            print("Worker processing job. Terminate worker with CTRL+C")
            
            worker_task()
            
            time.sleep(seconds)
        except KeyboardInterrupt:
            break;

def migrations():
    """
    This will clear the existing database if it exists and run database migrations
    then fill it with seeder data
    """
    clearMigrateSeed()

def main():
    print("Run as:\n")

    print("[1] Worker")
    print("[2] Migrations")
    print("[any other key] to exit")

    string_input = input("\nChoice: ")
    run_as = int(string_input)

    if run_as == 1:
        worker()
    elif run_as == 2:
        migrations()

        connection = database()
        worker_job(connection)
        connection.close()

if __name__ == "__main__":
    main()
