from grpc import Channel
import grpc

from BankingApp_pb2_grpc import BankingAppStub
from BankingApp_pb2 import LoginRequest, LoginResponse


class BasService:
    channel: Channel
    connectionString: str
    stub: BankingAppStub

    def __init__(self, basConnectionString: str):
        self.connectionString = basConnectionString

        self.channel = grpc.insecure_channel(self.connectionString)
        self.stub = BankingAppStub(self.channel)

    def login(self, username: str , password: str) -> str:
        response: LoginResponse = self.stub.Login(LoginRequest(username=username, password=password))

        if response.success is False:
            raise BaseException("Login failed")

        return response.token
    
    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
