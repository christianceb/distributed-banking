from typing import Optional

from BasService import BasService
from CurrencyHelper import int_cents_to_localised
from Common import unix_timestamp_s, unix_timestamp_to_iso8601
from Models import SessionData, Transaction, User
from Utils import render_txn_amount


class CliApplication:
    MENU_WAITING_INPUT: str = "WAIT"
    MENU_EXIT: str = "x"

    bas_service: BasService = None
    session_data: SessionData = None

    def __init__(self, basService: BasService):
        self.bas_service = basService

        self.entrypoint()

    def entrypoint(self):
        self.login()

    def login(self):
        while self.session_data is None:
            username_input = ""
            password_input = ""
            
            username_input = input("\nEnter username: ")
            password_input = input("Enter password: ")

            try:
                login_response = self.bas_service.login(username_input, password_input)
                
                self.session_data = SessionData()

                self.session_data.user_id = login_response.user_id
                self.session_data.account_id = login_response.account_id
                self.session_data.token = login_response.token

                self.session_data.user = User()
                self.session_data.user.id = login_response.user.id
                self.session_data.user.username=login_response.user.username

                break;
            except:
                print("\nFailed to login. Check credentials.\n\n---")

                continue

        self.mainMenu()

    def printAccountOverview(self):
        overview = self.bas_service.get_account_by_token(self.session_data.token)

        print("Logged in as: " + self.session_data.user.username)
        print("Balances as of: " + unix_timestamp_to_iso8601(unix_timestamp_s()))
        print("Account current balance: " + int_cents_to_localised(overview.current_balance))
        print("Account available balance: " + int_cents_to_localised(overview.available_balance))

    def printTransactions(self):
        pass

    def mainMenu(self):
        keyboard_interrupt = False

        MAIN_MENU = "1"
        VIEW_TRANSACTIONS = "2"
        MAKE_PAYMENT = "3"

        valid_options = [MAIN_MENU, VIEW_TRANSACTIONS, MAKE_PAYMENT, self.MENU_EXIT]

        menu_options: list[str] = [
            "[1] Reload this screen (refresh balance)",
            "[2] View Transactions",
            "[3] Make a payment",
            "[X] Exit Application"
        ]

        choice: str = self.MENU_WAITING_INPUT

        while choice is self.MENU_WAITING_INPUT:
            if keyboard_interrupt:
                break

            print("\n---\n")

            self.printAccountOverview()

            print("\n---\n")

            print("What do you want to do?\n")

            for menu_option in menu_options:
                print("- " + menu_option)

            while choice is self.MENU_WAITING_INPUT:
                if keyboard_interrupt:
                    break

                try:
                    choice = input("\nEnter choice: ").lower()
                except KeyboardInterrupt:
                    keyboard_interrupt = True
                    break
                except:
                    choice = self.MENU_WAITING_INPUT

                if choice not in valid_options: 
                    print("Choice entered invalid. Try again.")

            if choice == MAIN_MENU:
                print("\nReloading account overview...")

                choice = self.MENU_WAITING_INPUT
                continue

            elif choice == VIEW_TRANSACTIONS:
                self.viewTransactionsMenu()

            elif choice == MAKE_PAYMENT:
                self.makePayment()

            elif choice == self.MENU_EXIT:
                print("Bye!")
                break

            choice = self.MENU_WAITING_INPUT

    def printTransactionsHeaders(self):
        headers: list[tuple[str, int]] = []

        headers.append(("Transaction Id", 1))
        headers.append(("Amount", 2))
        headers.append(("Status", 1))
        headers.append(("Balance", 2))
        headers.append(("Kind", 2))
        headers.append(("Date/Time", 1))

        for header in headers:
            print(f"{header[0]}" + ("\t"*header[1]), end="")

    def viewTransactionsMenu(self):
        REFRESH_SCREEN = "r"
        VIEW_TRANSACTION = "v"
        valid_options = [REFRESH_SCREEN, VIEW_TRANSACTION, self.MENU_EXIT]

        menu_options: list[str] = [
            "[R] Reload this transaction screens",
            "[V] View a Transaction by Transaction ID",
            "[X] Go back to main menu"
        ]

        choice = self.MENU_WAITING_INPUT

        while choice is self.MENU_WAITING_INPUT:
            print("\n---")
            
            print("Viewing Transactions")

            transactions: list[Transaction] = self.bas_service.get_transactions_by_token(self.session_data.token)

            self.printTransactionsHeaders()

            print("\n---")

            for transaction in transactions:
                print(
                    str(transaction.id) + "\t",
                    render_txn_amount(transaction, self.session_data.account_id),
                    transaction.status,
                    str(transaction.balance) + "\t",
                    transaction.kind,
                    unix_timestamp_to_iso8601(transaction.timestamp),
                    sep="\t", end=None
                )

            while choice is self.MENU_WAITING_INPUT:
                print("\n---")

                print("What do you want to do?\n")

                for menu_option in menu_options:
                    print("- " + menu_option)

                try:
                    choice = input("\nEnter choice: ").lower()
                except KeyboardInterrupt as error:
                    raise error
                except:
                    choice = self.MENU_WAITING_INPUT

                if choice not in valid_options: 
                    print("Choice entered invalid. Try again.")

            if choice == self.MENU_EXIT:
                print("\nLeaving View Transactions")
                break
            elif choice == REFRESH_SCREEN:
                print("\Reloading View Transactions")
                choice = self.MENU_WAITING_INPUT
                continue
            elif choice == VIEW_TRANSACTION:
                self.viewTransaction()

            choice = self.MENU_WAITING_INPUT

    def viewTransaction(self):
        print("\n---")

        input("Enter Transaction ID to view: ")

    def makePayment(self):
        PAYMENT_INTENT_PROMPT = 10000
        SHOW_ESTIMATE_AND_CONFIRM = 11000
        CANCEL_PAYMENT_INTENT = 12000
        PAYMENT_INTENT_SUBMITTED = 13000

        pass
