from bdb.main import app as bdb_app
from bas.main import app as bas_app


def main():
    print("Run:\n")

    print("[1] BDB")
    print("[2] BDB Migrations")
    print("[3] BAS")
    print("[4] BC")

    print("[any other key] to exit")

    string_input = input("\nChoice: ")
    run_as = int(string_input)

    if run_as == 1:
        bdb_app()
    elif run_as == 2:
        pass
    elif run_as == 3:
        bas_app()
    elif run_as == 4:
        pass

if __name__ == "__main__":
    main()
