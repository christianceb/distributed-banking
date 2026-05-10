import grpc
from typing import Optional
from InternalBanking_pb2_grpc import InternalBankingStub
from InternalBanking_pb2 import UserCredentialsRequest, UserResponse


class BankingDatabaseService:
    channel: grpc.Channel
    connection_string: str
    stub: InternalBankingStub

    def __init__(self, bdb_connection_string: str):
        self.connection_string = bdb_connection_string

        self.channel = grpc.insecure_channel(self.connection_string)
        self.stub = InternalBankingStub(self.channel)

        print("BAS is listening to BDB via " + bdb_connection_string)

    def validate_user(self, username: str , password: str):
        request: UserResponse =  self.stub.GetUserRecordsByCredentials(UserCredentialsRequest(username=username, password=password))

        return request if request.found else None
    
    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
