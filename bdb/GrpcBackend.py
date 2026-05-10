import sqlite3

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

    db_connection: sqlite3.Connection

    def __init__(self):
        self.init_data_store()
        
        # sqlite3 does not like multithreaded access to a data store, so they
        # need to be put inside the only thread that can use it
        self.banking_service = BankingService(self.db_connection)

    # @interceptor
    def GetUserRecordsByCredentials(self, request: UserCredentialsRequest, context) -> UserResponse:
        response = UserResponse()

        user = self.banking_service.validate_user(request.username, request.password)

        response.found = False
        response.user = None
        response.account = None
        response.transactions = []
        
        if user is not None:
            response.found = True
            response.user.id = user.id
            
            # TBD
            # response.account.id = account.id
            # response.account.current_balance = account.current_balance
            # response.account.available_balance = account.available_balance
            # response.account.updated_at = account.updated_at

            # response.transactions = []

        return response

    def init_data_store(self):
        self.db_connection = sqlite3.connect("store.db")

    def close_data_store_connection(self):
        # TODO need to figure out end of grpc lifecycle to call this
        self.db_connection.close()
