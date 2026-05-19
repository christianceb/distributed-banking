from grpc import Channel
import grpc

from BankingApp_pb2_grpc import BankingAppStub
from BankingApp_pb2 import LoginRequest, LoginResponse, PublicAccountDetailsRequest, PublicAccountDetailsResponse, TransactionsRequest, TransactionsResponse
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

    def get_transactions_by_token(self, token: str):
        request: TransactionsRequest = TransactionsRequest(token=token)
        response: TransactionsResponse = self.stub.GetTransactionsByToken(request)

        transactions: list[Transaction] = []

        for response_transaction in response.transactions:
            transaction = Transaction()

            transaction.id = response_transaction.id
            transaction.amount = response_transaction.amount
            transaction.source_account_id = response_transaction.source_account_id
            transaction.destination_account_id = response_transaction.destination_account_id
            transaction.message = response_transaction.message
            transaction.status = response_transaction.status
            transaction.balance = response_transaction.balance
            transaction.fees = response_transaction.fees
            transaction.kind = response_transaction.kind
            transaction.timestamp = response_transaction.timestamp

            transactions.append(transaction)

        return transactions

    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
