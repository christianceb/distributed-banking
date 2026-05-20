from typing import Optional
from BankingApp_pb2 import EvaluatePaymentIntentResponse, LoginRequest, LoginResponse, PublicAccountDetailsRequest, PublicAccountDetailsResponse, PublicPaymentIntentRequest, TransactionRequest, TransactionsResponse
from BankingApp_pb2_grpc import BankingAppServicer
from UserTokenService import UserToken, UserTokenService
from BankingDatabaseService import BankingDatabaseService
from Utils import calculate_fees

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

    def GetTransactionById(self, request: TransactionRequest, context) -> TransactionsResponse:
        pass

    def EvaluatePaymentIntent(self, request: PublicPaymentIntentRequest, context) -> EvaluatePaymentIntentResponse:
        user_token = self.ValidateToken(request.token)
        fees = 0
        valid_payment_intent = False

        if request.amount > 0:
            if user_token and user_token.account_id != request.recipient_account_id:
                if self.data_service.account_by_id_exists(request.recipient_account_id):
                    valid_payment_intent = True
            
        if valid_payment_intent:
            fees = calculate_fees(amount=request.amount)

        return EvaluatePaymentIntentResponse(valid_payment_intent=True, fees=fees)
