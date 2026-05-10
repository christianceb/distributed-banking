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

        user_response = self.data_service.validate_user(request.username, request.password)

        response.token = ""
        response.success = False

        if user_response is not None:
            response.token = self.user_token_service.GenerateUserToken(user_response.user, [str(user_response.user), request.username, request.password])
            response.success = True

        return response

    def ValidateToken(self, token) -> Optional[UserToken]:
        return self.user_token_service.FindToken(token)

    def GetAccountDetailsByToken(self, request: PublicAccountDetailsRequest, context) -> PublicAccountDetailsResponse:
        pass

    def GetTransactionsByToken(self, request: TransactionsRequest, context) -> TransactionsResponse:
        pass

    def GetTransactionById(self, request: TransactionRequest, context) -> TransactionsResponse:
        pass
