import sqlite3

def createAccountTriggers():
    """
    --- Reference: https://stackoverflow.com/questions/6578439/on-update-current-timestamp-with-sqlite
    CREATE TRIGGER update_account_timestamp UPDATE OF current_balance, available_balance ON accounts
        BEGIN
            UPDATE accounts SET updated_at = unixepoch('now','subsec') WHERE accounts.id = old.id AND accounts.updated_at = old.updated_at;
        END;
    """
    pass

def createAccounts():
    """
    create table accounts
    (
        id                integer                        not null
            constraint accounts_id_pk
                primary key autoincrement,
        user_id           integer
            constraint accounts___user_id_fk
                references users,
        current_balance   integer                        not null,
        available_balance integer                        not null,
        updated_at        unixepoch default unixepoch('now','subsec') * 1000 not null
    );
    """
    pass

def createUsers():
    """
    create table users
    (
        id       integer not null
            constraint users_id_pk
                primary key autoincrement,
        username varchar(255) not null,
        password varchar(255) not null,
        token    integer # we don't need to handle tokens in BDB, do it instead in BAS as in-memory
    );
    """
    pass

def openDataStore():
    sqlite3.connect("store.db")

def main():
    openDataStore()

if __name__ == "__main__":
    main()
