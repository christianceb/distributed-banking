from BankingService import BankingService
from InternalBanking_pb2_grpc import InternalBankingServicer
from InternalBanking_pb2 import AccountByUserIdResponse, AccountByUserIdRequest, InternalTransactionsByAccountIdRequest, InternalTransactionsResponse, UserByCredentialsRequest, UserByCredentialsResponse
from Common import Transaction

def interceptor(func):
    def inner(*args, **kwargs):
        print("Replacement for worker goes here")
        return func(*args, **kwargs)

    return inner

class GrpcBackend(InternalBankingServicer):
    banking_service: BankingService

    def __init__(self):
        self.banking_service = BankingService(None)

    def GetUserByCredentials(self, request: UserByCredentialsRequest, context) -> UserByCredentialsResponse:
        response = UserByCredentialsResponse()

        user = self.banking_service.get_user_by_username_password(request.username, request.password)

        response.found = False

        if user is not None:
            response.found = True
            response.user.id = user.id

            # There currently is a 1:1 relationship with user and account
            account = self.banking_service.get_account_by_user_id(user.id)

            # TODO when returning account, don't use sqlite row. Instead, put then in a class
            response.account.id = account['id']
            response.account.current_balance = account['current_balance']
            response.account.available_balance = account['available_balance']
            response.account.updated_at = account['updated_at']

            response.user.id = user.id
            response.user.username = user.username
            
            # May need to transform this
            response.transactions.extend([])
            # response.transactions = [self.banking_service.get_transactions_by_account_id(account['id'])]

        return response

    def GetAccountByUserId(self, request: AccountByUserIdRequest, context) -> AccountByUserIdResponse:
        response = AccountByUserIdResponse()

        account = self.banking_service.get_account_by_user_id(request.user_id)

        response.account.id = account['id']
        response.account.user_id = account['user_id']
        response.account.current_balance = account['current_balance']
        response.account.available_balance = account['available_balance']
        response.account.updated_at = account['updated_at']

        return response

    def GetTransactionsByAccountId(self, request: InternalTransactionsByAccountIdRequest, context) -> InternalTransactionsResponse:
        response = InternalTransactionsResponse()

        transaction_rows: list[Transaction] = self.banking_service.get_transactions_by_account_id(request.account_id)

        for transaction_row in transaction_rows:
            transaction = Transaction()
            
            response.transactions.add(
                id = transaction_row['id'],
                amount = transaction_row['amount'],
                source_account_id = transaction_row['source_account_id'],
                destination_account_id = transaction_row['destination_account_id'],
                message = transaction_row['message'],
                status = transaction_row['status'],
                balance = transaction_row['balance'],
                fees = transaction_row['fees'],
                kind = transaction_row['kind'],
                # tries = transaction_row['tries'],
                timestamp = transaction_row['timestamp'],
                # updated_at = transaction_row['updated_at'],
            )

        return response
