import grpc
from typing import Optional
from InternalBanking_pb2_grpc import InternalBankingStub
from InternalBanking_pb2 import AccountResponse, GetAccountByUserIdRequest, UserCredentialsRequest, UserResponse


class BankingDatabaseService:
    channel: grpc.Channel
    connection_string: str
    stub: InternalBankingStub

    def __init__(self, bdb_connection_string: str):
        self.connection_string = bdb_connection_string

        self.channel = grpc.insecure_channel(self.connection_string)
        self.stub = InternalBankingStub(self.channel)

        print("BAS is listening to BDB via " + bdb_connection_string)

    def validate_user(self, username: str , password: str) -> UserResponse:
        request: UserCredentialsRequest = UserCredentialsRequest(username=username, password=password)
        response: UserResponse = self.stub.GetUserRecordsByCredentials(request)

        return response if response.found else None
    
    def get_account_by_user_id(self, user_id: int) -> AccountResponse:
        request: GetAccountByUserIdRequest = GetAccountByUserIdRequest(user_id=user_id)
        response: AccountResponse = self.stub.GetAccountByUserId(request)

        return response


    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
