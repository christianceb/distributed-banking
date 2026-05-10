from BasService import BasService
from CurrencyHelper import int_cents_to_localised


class CliApplication:
    WAITING_INPUT: int = 0
    
    EXIT: int = 100000
    EXIT_AS_STRING: str = "x"

    bas_service: BasService = None
    session_token = None

    def __init__(self, basService: BasService):
        self.bas_service = basService

        self.entrypoint()

    def entrypoint(self):
        self.login()

    def login(self):
        while self.session_token is None:
            username_input = ""
            password_input = ""
            
            username_input = input("\nEnter username: ")
            password_input = input("Enter password: ")

            try:
                self.session_token = self.bas_service.login(username_input, password_input)

                break;
            except:
                print("Failed to login. Check credentials.")
                continue

        print("\nLogged in as: " + "REPLACE_WITH_USERNAME")

        self.mainMenu()

    def printAccountOverview(self):
        overview = self.bas_service.get_account_by_token(self.session_token)

        print("Account current balance: " + int_cents_to_localised(overview.current_balance))
        print("Account available balance: " + int_cents_to_localised(overview.available_balance))

    def printTransactions(self):
        pass

    def mainMenu(self):
        keyboard_interrupt = False

        MAIN_MENU = 1
        VIEW_TRANSACTIONS = 2
        MAKE_PAYMENT = 3

        valid_options = [MAIN_MENU, VIEW_TRANSACTIONS, MAKE_PAYMENT, self.EXIT]

        menu_options: list[str] = [
            "[1] Reload this screen (refresh balance)",
            "[2] View Transactions",
            "[3] Make a payment",
            "[X] Exit Application"
        ]

        choice: int = self.WAITING_INPUT

        while choice is self.WAITING_INPUT:
            if keyboard_interrupt:
                break

            print("\n---\n")

            self.printAccountOverview()

            print("\n---\n")

            print("What do you want to do?\n")

            for menu_option in menu_options:
                print("- " + menu_option)

            while choice is self.WAITING_INPUT:
                if keyboard_interrupt:
                    break

                try:
                    string_choice = input("\nEnter choice: ")

                    if str.lower(string_choice) == self.EXIT_AS_STRING:
                        choice = self.EXIT
                    else:
                        choice: int = int(string_choice)
                except KeyboardInterrupt:
                    keyboard_interrupt = True
                    break
                except:
                    choice = self.WAITING_INPUT

                if choice not in valid_options: 
                    print("Choice entered invalid. Try again.")

            if choice is MAIN_MENU:
                print("Reloading account overview...")

            elif choice is VIEW_TRANSACTIONS:
                self.viewTransactionsMenu()

            elif choice is MAKE_PAYMENT:
                self.makePayment()

            elif choice is self.EXIT:
                print("Bye!")
                break;

            choice = self.WAITING_INPUT

    def viewTransactionsMenu(self):
        REFRESH_SCREEN = "r"
        VIEW_TRANSACTION = "v"

        valid_options = [REFRESH_SCREEN, VIEW_TRANSACTION, self.EXIT]

        menu_options: list[str] = [
            "[R] Reload this transaction screen",
            "[V] View a Transaction by Transaction ID",
            "[X] Go back to main menu"
        ]
        pass;

    def makePayment(self):
        PAYMENT_INTENT_PROMPT = 10000
        SHOW_ESTIMATE_AND_CONFIRM = 11000
        CANCEL_PAYMENT_INTENT = 12000
        PAYMENT_INTENT_SUBMITTED = 13000

        pass
