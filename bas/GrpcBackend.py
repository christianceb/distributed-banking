from typing import Optional
from BankingApp_pb2 import LoginRequest, LoginResponse, PublicAccountDetailsRequest, PublicAccountDetailsResponse, TransactionRequest, TransactionsRequest, TransactionsResponse
from BankingApp_pb2_grpc import BankingAppServicer
from UserTokenService import UserToken, UserTokenService
from BankingDatabaseService import BankingDatabaseService

class GrpcBackend(BankingAppServicer):
    data_service: BankingDatabaseService = None;
    user_token_service: UserTokenService = None

    def __init__(self, dataService, userTokenService):
        self.data_service = dataService
        self.user_token_service = userTokenService

    def Login(self, request: LoginRequest, context) -> LoginResponse:
        response = LoginResponse()

        user_validation_result = self.data_service.validate_user(request.username, request.password)

        response.token = ""
        response.success = False

        if user_validation_result is not None:
            user = user_validation_result.user

            response.user_id = user_validation_result.user.id
            response.account_id = user_validation_result.account.id

            user_token = self.user_token_service.GenerateUserToken(
                user_validation_result.user.id,
                user_validation_result.account.id,
                [str(user_validation_result.user.id), request.username, request.password]
            )

            response.token = user_token.token

            response.user.id = user.id
            response.user.username = user.username

            response.success = True

        return response

    def ValidateToken(self, token) -> Optional[UserToken]:
        return self.user_token_service.FindToken(token)

    def GetAccountDetailsByToken(self, request: PublicAccountDetailsRequest, context) -> PublicAccountDetailsResponse:
        response = PublicAccountDetailsResponse();
    
        user_token = self.ValidateToken(request.token)

        if user_token is not None:
            data_service_response = self.data_service.get_account_by_user_id(user_token.user_id)
            account = data_service_response.account

            response.account.id = account.id
            response.account.user_id = account.user_id
            response.account.current_balance = account.current_balance
            response.account.available_balance = account.available_balance
            response.account.updated_at = account.updated_at

        return response

    def GetTransactionsByToken(self, request: TransactionsRequest, context) -> TransactionsResponse:
        user_token = self.ValidateToken(request.token)

        if user_token is not None:
            return self.data_service.get_transactions_by_account_id(user_token.account_id)

    def GetTransactionById(self, request: TransactionRequest, context) -> TransactionsResponse:
        pass
