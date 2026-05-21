import grpc
from typing import Optional
from InternalBanking_pb2_grpc import InternalBankingStub
from InternalBanking_pb2 import AccountByIdExistsRequest, AccountByIdExistsResponse, AccountByUserIdResponse, AccountByUserIdRequest, AccountTransactionRequest, TransactionsResponse, PaymentIntentRequest, PaymentIntentResponse, UserByCredentialsRequest, UserByCredentialsResponse
from Models import Transaction


class BankingDatabaseService:
    channel: grpc.Channel
    connection_string: str
    stub: InternalBankingStub

    def __init__(self, bdb_connection_string: str):
        self.connection_string = bdb_connection_string

        self.channel = grpc.insecure_channel(self.connection_string)
        self.stub = InternalBankingStub(self.channel)

        print("BAS is listening to BDB via " + bdb_connection_string)

    def validate_user(self, username: str , password: str) -> UserByCredentialsResponse:
        request: UserByCredentialsRequest = UserByCredentialsRequest(username=username, password=password)
        response: UserByCredentialsResponse = self.stub.GetUserByCredentials(request)

        return response if response.found else None
    
    def get_account_by_user_id(self, user_id: int) -> AccountByUserIdResponse:
        request: AccountByUserIdRequest = AccountByUserIdRequest(user_id=user_id)
        response: AccountByUserIdResponse = self.stub.GetAccountByUserId(request)

        return response

    def get_account_transaction_with_id(self, account_id: int, transaction_id: int) -> Optional[Transaction]:
        request: AccountTransactionRequest = AccountTransactionRequest(account_id=account_id, transaction_id=transaction_id)
        response: TransactionsResponse = self.stub.GetAccountTransactionWithId(request)

        if len(response.transactions):
            transaction = Transaction()

            # TODO populate with data

            return transaction

        return None

    def account_by_id_exists(self, account_id: int) -> bool:
        request: AccountByIdExistsRequest = AccountByIdExistsRequest(id=account_id)
        response: AccountByIdExistsResponse = self.stub.AccountByIdExists(request)

        return response.exists

    def post_payment_intent(self, account_id: int, recipient_account_id: int, fees: int, amount: int, message: str) -> Optional[Transaction]:
        request: PaymentIntentRequest = PaymentIntentRequest(account_id=account_id, recipient_account_id=recipient_account_id, fees=fees, amount=amount, message=message)
        response: PaymentIntentResponse = self.stub.StorePaymentIntent(request)

        if response.transaction:
            transaction = Transaction()
            return transaction
        
        return None

    def __del__(self):
        # Prevent dangling connections which may exhaust connection pool threads
        self.channel.close()
