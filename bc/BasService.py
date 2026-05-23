import grpc

from typing import Optional
from grpc import Channel
from grpc_generated.BankingApp_pb2_grpc import BankingAppStub
from grpc_generated.BankingApp_pb2 import AppTransaction, AppTransactionRequest, AppTransactionsResponse, EvaluatePaymentIntentResponse, LoginRequest, LoginResponse, AppPaymentIntentRequest, AppAccountDetailsRequest, AppAccountDetailsResponse, AppPaymentIntentStoreResponse, AppPostPaymentIntentRequest
from models.PublicTransactionModel import PublicTransactionModel


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

    def get_transaction(self, token: str, transaction_id: int) -> Optional[PublicTransactionModel]:
        request: AppTransactionRequest = AppTransactionRequest(token=token, transaction_id=transaction_id)
        response: AppTransactionsResponse = self.stub.GetTransactionById(request)

        if len(response.transactions):
            transaction = self.from_protoc_transaction_to_object(response.transactions[0])

            return transaction
        
        return None

    def validate_and_get_payment_intent_fees(self, token: str, recipient_account_id: int, amount: int) -> Optional[int]:
        request = AppPaymentIntentRequest(token=token, recipient_account_id=recipient_account_id, amount=amount)
        response: EvaluatePaymentIntentResponse = self.stub.EvaluatePaymentIntent(request)

        if response.valid_payment_intent:
            return response.fees

        return None

    def post_payment_intent(self, token: str, recipient_account_id: int, amount: int, message: str = "") -> Optional[PublicTransactionModel]:
        request = AppPostPaymentIntentRequest(token=token, recipient_account_id=recipient_account_id, amount=amount, message=message)
        response: AppPaymentIntentStoreResponse = self.stub.PostPaymentIntent(request)

        if response.transaction:
            transaction = self.from_protoc_transaction_to_object(response.transaction)

            return transaction

        return None

    def from_protoc_transaction_to_object(self, protoc_transaction: AppTransaction) -> PublicTransactionModel:
        transaction = PublicTransactionModel()
    
        transaction.id = protoc_transaction.id
        transaction.source_account_id = protoc_transaction.source_account_id
        transaction.recipient_account_id = protoc_transaction.recipient_account_id
        transaction.amount = protoc_transaction.amount
        transaction.status = protoc_transaction.status
        transaction.fees = protoc_transaction.fees
        transaction.kind = protoc_transaction.kind
        transaction.timestamp = protoc_transaction.timestamp
        transaction.updated_at = protoc_transaction.updated_at
    
        return transaction

    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
