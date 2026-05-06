from bc import BasService


class CliApplication:
    WAITING_INPUT: int = 0
    
    EXIT: int = 100000
    EXIT_AS_STRING: str = "x"

    basService = None
    session = None

    def __init__(self, basService: BasService):
        self.basService = basService

        self.entrypoint()

    def entrypoint(self):
        self.login()

    def login(self):
        while self.session is None:
            username_input = "", password_input = ""
            
            username_input = input("\nEnter username: ")
            password_input = input("\nEnter password: ")

            

    def printAccountOverview(self):
        pass

    def printTransactions(self):
        pass

    def mainMenu(self):
        MAIN_MENU = 1
        VIEW_TRANSACTIONS = 2
        MAKE_PAYMENT = 3

        valid_options = [MAIN_MENU, VIEW_TRANSACTIONS, MAKE_PAYMENT, self.EXIT]

        menu_options: list[str] = [
            "[1] Reload this screen (refresh balance)",
            "[2] View Transactions",
            "[4] Make a payment",
            "[X] Exit Application"
        ]

        choice: int = self.WAITING_INPUT

        while choice is self.WAITING_INPUT:
            print("\n---\n")

            self.printAccountOverview()

            print("\n---\n")

            print("What do you want to do?\n")

            for menu_option in menu_options:
                print("- " + menu_option)

            while choice is self.WAITING_INPUT:
                try:
                    string_choice = input("\nEnter choice: ")

                    if str.lower(choice) is self.EXIT_AS_STRING:
                        choice = self.EXIT
                    else:
                        choice: int = int(string_choice)
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
