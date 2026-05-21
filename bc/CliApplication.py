from typing import Optional

from BasService import BasService
from CurrencyHelper import inputted_amount_to_cents, int_cents_to_localised
from Temporal import unix_timestamp_s, unix_timestamp_to_iso8601
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
        VIEW_TRANSACTION = "2"
        MAKE_PAYMENT = "3"

        valid_options = [MAIN_MENU, VIEW_TRANSACTION, MAKE_PAYMENT, self.MENU_EXIT]

        menu_options: list[str] = [
            "[1] Reload this screen (refresh balance)",
            "[2] View Transaction",
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

            elif choice == VIEW_TRANSACTION:
                self.view_transaction()

            elif choice == MAKE_PAYMENT:
                self.make_payment()

            elif choice == self.MENU_EXIT:
                print("Bye!")
                break

            choice = self.MENU_WAITING_INPUT

    def view_transaction(self):
        print("\n---\n")

        exit_menu_loop = None

        while exit_menu_loop != self.MENU_EXIT:
            try:
                transaction_id = int(input("Enter Transaction ID to view: "))
            except:
                continue
            
            transaction = self.bas_service.get_transaction(self.session_data.token, transaction_id)

            if transaction is None:
                print("\nCould not load this transaction")
            else:
                self.print_transaction(transaction)

            input("\nPress [enter] to go back")

            exit_menu_loop = self.MENU_EXIT

    def print_transaction(self, transaction: Transaction):
        print(f"""
            ---
            Transaction ID: {transaction.id}
            Amount: {transaction.amount}
            Source Account ID: {transaction.source_account_id}
            Destination Account ID: {transaction.destination_account_id}
            Status: {transaction.status}
            Balance: {transaction.balance}
            Fees: {transaction.fees}
            Kind: {transaction.fees}
            Timestamp: {transaction.timestamp}
            ---
        """)

    def make_payment(self):
        choice: str = self.MENU_WAITING_INPUT

        while choice is self.MENU_WAITING_INPUT:
            print("\n---\n")

            payment_intent_valid = False

            input_recipient_account_id = input("Enter recipient account ID: ")
            input_amount_to_transfer = input("Enter amount to transfer: ")
            input_message = input("Enter message [optional]: ")

            # Validate input by casting
            try:
                recipient_account_id = int(input_recipient_account_id)
                transfer_amount = inputted_amount_to_cents(float(input_amount_to_transfer))
            except:
                print("\nInvalid inputs provided. Try again.")
                continue
            
            message = input_message

            payment_intent = self.bas_service.validate_payment_intent(self.session_data.token, recipient_account_id, transfer_amount)

            if not payment_intent.valid_payment_intent:
                print("Unable to continue with transaction. Either the recipient is invalid, or you do not have enough funds to make the transaction.")
            else:
                transfer_total = transfer_amount + payment_intent.fees

                print("\nPayment will be sent to account with ID: " + str(recipient_account_id))
                print("Transfer amount: " + int_cents_to_localised(transfer_amount))
                print("Transfer fee: " + int_cents_to_localised(payment_intent.fees))
                print("Total transfer (incl fees): " + int_cents_to_localised(transfer_total))
                print("Message: " + message)

                valid_confirm_input = False

                while valid_confirm_input is False:
                    try:
                        confirm = input("\nConfirm and submit payment? [y/n]: ").lower()
                    except:
                        continue

                    if confirm == "n":
                        valid_confirm_input = True
                        choice = self.MENU_EXIT
                        print("\nCancelling payment. Returning to Main Menu")
                        continue
                    elif confirm == "y":
                        valid_confirm_input = True

                        self.bas_service.post_payment_intent(
                            self.session_data.token,
                            recipient_account_id,
                            transfer_amount,
                            message
                        )

                        print("Your payment has been received")
                        print("Transfer amount: 100.10")
                        print("Transfer fee: 0.10")
                        print("Message: hi!")
