from bdb.main import app as bdb_app
from bdb.worker import worker, migrations
from bas.main import app as bas_app
from bc.main import app as bc_app


def main():
    print("Run:\n")

    print("[1] BDB")
    print("[2] BAS")
    print("[3] BC")
    print("[4] BDB Migrations")
    print("[5] BDB Worker (Advanced)")

    print("[any other key] to exit")

    string_input = input("\nChoice: ")
    run_as = int(string_input)

    if run_as == 1:
        bdb_app()
    elif run_as == 2:
        bas_app()
    elif run_as == 3:
        string_input = input("\nEnter IP:Port of BAS to connect to [localhost:10051]: ")

        if string_input == "":
            bc_app()
        else:
            bc_app(string_input)

    elif run_as == 4:
        migrations()
    elif run_as == 5:
        worker()

if __name__ == "__main__":
    main()
