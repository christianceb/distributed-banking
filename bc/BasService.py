from grpc import Channel
import grpc

from BankingApp_pb2_grpc import BankingAppStub
from BankingApp_pb2 import LoginRequest, LoginResponse, PublicAccountDetailsRequest, PublicAccountDetailsResponse


class BasService:
    channel: Channel
    connection_string: str
    stub: BankingAppStub

    def __init__(self, bas_connection_string: str):
        self.connection_string = bas_connection_string

        self.channel = grpc.insecure_channel(self.connection_string)
        self.stub = BankingAppStub(self.channel)

    def login(self, username: str , password: str) -> str:
        response: LoginResponse = self.stub.Login(LoginRequest(username=username, password=password))

        if response.success is False:
            raise BaseException("Login failed")

        return response.token
    
    def get_account_by_token(self, token: str):
        response: PublicAccountDetailsResponse = self.stub.Login(PublicAccountDetailsRequest(token=token))

        if len(response.accounts):
            return response.accounts[0]

        return None

    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
