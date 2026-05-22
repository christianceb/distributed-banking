from BankingService import BankingService
from InternalBanking_pb2_grpc import InternalBankingServicer
from InternalBanking_pb2 import AccountByIdExistsRequest, AccountByIdExistsResponse, AccountByUserIdResponse, AccountByUserIdRequest, AccountTransactionRequest, PaymentIntentRequest, PaymentIntentResponse, TransactionsResponse, UserByCredentialsRequest, UserByCredentialsResponse


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

    def AccountByIdExists(self, request: AccountByIdExistsRequest, context) -> AccountByIdExistsResponse:
        response = AccountByIdExistsResponse()

        if self.banking_service.get_account(request.id):
            response.exists = True
        else:
            response.exists = False

        return response

    def GetAccountTransactionWithId(self, request: AccountTransactionRequest, context) -> TransactionsResponse:
        response = TransactionsResponse()

        transaction = self.banking_service.get_account_transaction_with_id(request.account_id, request.transaction_id)

        if transaction:
            response.transactions.add(
                id = transaction['id'],
                amount = transaction['amount'],
                source_account_id = transaction['source_account_id'],
                recipient_account_id = transaction['recipient_account_id'],
                message = transaction['message'],
                status = transaction['status'],
                fees = transaction['fees'],
                kind = transaction['kind'],
                timestamp = transaction['timestamp'],
                updated_at = transaction['updated_at'],
            )

        return response

    def StorePaymentIntent(self, request: PaymentIntentRequest, context) -> PaymentIntentResponse:
        response = PaymentIntentResponse()

        transaction = self.banking_service.new_transaction(
            request.account_id,
            request.recipient_account_id,
            request.amount,
            request.fees,
            request.message
        )

        if transaction:
            response.transaction.id = transaction['id']
            response.transaction.amount = transaction['amount']
            response.transaction.source_account_id = transaction['source_account_id']
            response.transaction.recipient_account_id = transaction['recipient_account_id']
            response.transaction.message = transaction['message']
            response.transaction.status = transaction['status']
            response.transaction.fees = transaction['fees']
            response.transaction.kind = transaction['kind']
            response.transaction.timestamp = transaction['timestamp']
            response.transaction.updated_at = transaction['updated_at']

        return response
