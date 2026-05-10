from BankingService import BankingService
from InternalBanking_pb2_grpc import InternalBankingServicer
from InternalBanking_pb2 import UserCredentialsRequest, UserResponse

def interceptor(func):
    def inner(*args, **kwargs):
        print("Replacement for worker goes here")
        return func(*args, **kwargs)

    return inner

class GrpcBackend(InternalBankingServicer):
    banking_service: BankingService

    def __init__(self):
        self.banking_service = BankingService(None)

    # @interceptor
    def GetUserRecordsByCredentials(self, request: UserCredentialsRequest, context) -> UserResponse:
        response = UserResponse()

        user_id = self.banking_service.validate_user(request.username, request.password)

        response.found = False

        if user_id is not None:
            response.found = True
            response.user.id = user_id

            # There currently is a 1:1 relationship with user and account
            account = self.banking_service.get_account_by_user_id(user_id)

            response.account.id = account['id']
            response.account.current_balance = account['current_balance']
            response.account.available_balance = account['available_balance']
            response.account.updated_at = account['updated_at']

            # May need to transform this
            response.transactions = []
            # response.transactions = [self.banking_service.get_transactions_by_account_id(account['id'])]

        return response
