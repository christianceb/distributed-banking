from grpc import Channel
import grpc

from BankingApp_pb2_grpc import BankingAppStub
from BankingApp_pb2 import EvaluatePaymentIntentResponse, LoginRequest, LoginResponse, PublicPaymentIntentRequest, PublicAccountDetailsRequest, PublicAccountDetailsResponse
from Models import Transaction


class BasService:
    channel: Channel
    connection_string: str
    stub: BankingAppStub

    def __init__(self, bas_connection_string: str):
        self.connection_string = bas_connection_string

        self.channel = grpc.insecure_channel(self.connection_string)
        self.stub = BankingAppStub(self.channel)

    def login(self, username: str , password: str) -> LoginResponse:
        response: LoginResponse = self.stub.Login(LoginRequest(username=username, password=password))

        if response.success is False:
            raise BaseException("Login failed")

        return response

    def get_account_by_token(self, token: str):
        request: PublicAccountDetailsRequest = PublicAccountDetailsRequest(token=token)
        response: PublicAccountDetailsResponse = self.stub.GetAccountDetailsByToken(request)

        if response.account is not None:
            return response.account

        return None

    def get_transaction(self, token: str, transaction_id: int) -> Transaction:
        pass

    def validate_payment_intent(self, token: str, recipient_account_id: int, amount: int):
        request = PublicPaymentIntentRequest(token=token, recipient_account_id=recipient_account_id, amount=amount)
        response: EvaluatePaymentIntentResponse = self.stub.EvaluatePaymentIntent(request)

        return response

    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
