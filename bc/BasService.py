from typing import Optional

from grpc import Channel
import grpc

from BankingApp_pb2_grpc import BankingAppStub
from BankingApp_pb2 import AppTransactionRequest, AppTransactionsResponse, EvaluatePaymentIntentResponse, LoginRequest, LoginResponse, AppPaymentIntentRequest, AppAccountDetailsRequest, AppAccountDetailsResponse, AppPaymentIntentStoreResponse, AppPostPaymentIntentRequest
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
        request: AppAccountDetailsRequest = AppAccountDetailsRequest(token=token)
        response: AppAccountDetailsResponse = self.stub.GetAccountDetailsByToken(request)

        if response.account is not None:
            return response.account

        return None

    def get_transaction(self, token: str, transaction_id: int) -> Optional[Transaction]:
        request: AppTransactionRequest = AppTransactionRequest(token=token, transaction_id=transaction_id)
        response: AppTransactionsResponse = self.stub.GetTransactionById(request)

        if len(response.transactions):
            transaction = Transaction()
            response_txn = response.transactions[0]

            transaction.id = response_txn.id
            transaction.source_account_id = response_txn.source_account_id
            transaction.destination_account_id = response_txn.destination_account_id
            transaction.amount = response_txn.amount
            transaction.bas = response_txn.bas
            transaction.status = response_txn.status
            transaction.balance = response_txn.balance
            transaction.fees = response_txn.fees
            transaction.kind = response_txn.kind
            transaction.tries = response_txn.tries
            transaction.timestamp = response_txn.timestamp
            transaction.updated_at = response_txn.updated_at

            return transaction
        
        return None

    def validate_payment_intent(self, token: str, recipient_account_id: int, amount: int):
        request = AppPaymentIntentRequest(token=token, recipient_account_id=recipient_account_id, amount=amount)
        response: EvaluatePaymentIntentResponse = self.stub.EvaluatePaymentIntent(request)

        return response

    def post_payment_intent(self, token: str, recipient_account_id: int, amount: int, message: str = "") -> Optional[Transaction]:
        request = AppPostPaymentIntentRequest(token=token, recipient_account_id=recipient_account_id, amount=amount, message=message)
        response: AppPaymentIntentStoreResponse = self.stub.PostPaymentIntent(request)

        if response.transaction:
            transaction = Transaction(
                # TODO
            )
            return transaction

        return None

    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
