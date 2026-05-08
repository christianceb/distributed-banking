import time

from migrations import clearMigrateSeed


def worker():
    seconds = 5

    print("Terminate worker with CTRL+C")

    while True:
        time.sleep(seconds)

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

    run_as = int(input("\nChoice: "))

    if run_as == 1:
        worker()
    elif run_as == 2:
        migrations()

if __name__ == "__main__":
    main()
