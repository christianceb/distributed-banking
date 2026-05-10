import os.path
import sqlite3

database_file = "store.db"

def clearMigrateSeed():
    """
    Clear
    """
    if os.path.exists(database_file):
        os.remove(database_file)

    """
    Migrate
    """
    connection = sqlite3.connect("store.db")

    connection.execute('pragma journal_mode=wal')

    cursor = connection.cursor()

    cursor.execute("""
        create table users
        (
            id integer not null constraint users_id_pk primary key autoincrement,
            username varchar(255) not null,
            password varchar(255) not null
        );
    """)
    connection.commit()

    cursor.execute("""
        create table accounts
        (
            id integer not null constraint accounts_id_pk primary key autoincrement,
            user_id integer constraint accounts_user_id_fk references users,
            current_balance integer not null,
            available_balance integer not null,
            updated_at unixepoch default (strftime('%s','now')) not null
        );
    """)
    connection.commit()

    cursor.execute("""
        create table transactions
        (
            id integer not null constraint transactions_pk primary key autoincrement,
            source_account_id integer constraint transactions_accounts_id_fk references accounts,
            destination_account_id integer not null constraint transactions_accounts_id_fk_2 references accounts,
            amount integer not null,
            status varchar(255) default 'PENDING' not null,
            balance integer,
            fee integer,
            kind varchar(255) not null,
            tries integer default 0 not null,
            timestamp unixepoch default (strftime('%s','now')) not null,
            updated_at unixepoch default (strftime('%s','now')) not null
        );
    """)
    connection.commit()

    cursor.execute("""
        create table logs
        (
            id integer not null constraint accounts_id_pk primary key autoincrement,
            kind varchar(255) not null,
            message text not null,
            timestamp unixepoch default (strftime('%s','now')) not null
        );
    """)
    connection.commit()

    # Triggers
    cursor.execute("""
        CREATE TRIGGER update_account_timestamp UPDATE OF current_balance, available_balance ON accounts
        BEGIN
            UPDATE accounts SET updated_at = (strftime('%s','now')) WHERE accounts.id = old.id AND accounts.updated_at = old.updated_at;
        END;
    """)

    cursor.execute("""
        CREATE TRIGGER update_transactions_timestamp UPDATE OF status, available_balance, tries ON transactions
        BEGIN
            UPDATE transactions SET updated_at = (strftime('%s','now')) WHERE transactions.id = old.id AND transactions.updated_at = old.updated_at;
        END;
    """)

    connection.commit()

    """
    Seed
    """
    cursor.execute("""
        insert into users
            (username, password)
        values
            ('bank', 'password1'),
            ('primary', 'password2'),
            ('secundus', 'password3');
    """)
    connection.commit()

    cursor.execute("""
        insert into accounts
            (user_id, current_balance, available_balance)
        values
            (?, ?, ?),
            (?, ?, ?),
            (?, ?, ?);
    """, (1, 0, 0, 2, 0, 0, 3, 0, 0))
    connection.commit()

    cursor.execute("""
        insert into transactions
            (destination_account_id, amount, kind)
        values
            (2, 100000, 'BROUGHT_FORWARD'),
            (3, 100000, 'BROUGHT_FORWARD');
    """)
    connection.commit()

    connection.close()

    print("Done.")
