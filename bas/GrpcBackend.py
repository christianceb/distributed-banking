from typing import Optional

from BankingApp_pb2 import LoginRequest, LoginResponse
from BankingApp_pb2_grpc import BankingAppServicer
from UserTokenService import UserToken, UserTokenService


class GrpcBackend(BankingAppServicer):
    data_service = None;
    user_token_service: UserTokenService = None

    def __init__(self, dataService, userTokenService):
        self.data_service = dataService
        self.user_token_service = userTokenService

    def Login(self, request: LoginRequest, context):
        response = LoginResponse()

        # TODO query data_service if user exists. For now, this is a pretend user
        data_service_response = {
            "id": 999
        }
        
        response.token = self.user_token_service.GenerateUserToken(data_service_response["id"], [request.username, request.password])

        response.success = True

        return response

    def ValidateToken(self, token) -> Optional[UserToken]:
        return self.user_token_service.FindToken(token)
