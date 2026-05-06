from BankingApp_pb2 import LoginRequest, LoginResponse
from BankingApp_pb2_grpc import BankingAppServicer


class GrpcBackend(BankingAppServicer):
    login_tokens = []
    dataService = None;

    def __init__(self, dataService):
        self.dataService = dataService
        print(self.dataService)

    def generateAuthToken(self, entropy: list[str]) -> str:
        return ";".join(entropy)

    def login(self, request: LoginRequest, context):
        response = LoginResponse()
        response.token = self.generateAuthToken([request.username, request.password])

        return response
