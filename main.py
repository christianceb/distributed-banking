from bdb.main import app


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
        app()
    elif run_as == 2:
        pass
    elif run_as == 3:
        pass
    elif run_as == 4:
        pass

if __name__ == "__main__":
    main()
