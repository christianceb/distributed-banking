from typing import Optional
from BankingApp_pb2 import AppTransactionRequest, EvaluatePaymentIntentResponse, LoginRequest, LoginResponse, AppAccountDetailsRequest, AppAccountDetailsResponse, AppPaymentIntentRequest, AppTransactionsResponse
from BankingApp_pb2_grpc import BankingAppServicer
from UserTokenService import UserToken, UserTokenService
from BankingDatabaseService import BankingDatabaseService
from Utils import calculate_fees
from Models import TransactionModel

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

    def GetAccountDetailsByToken(self, request: AppAccountDetailsRequest, context) -> AppAccountDetailsResponse:
        response = AppAccountDetailsResponse();
    
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

    def GetTransactionById(self, request: AppTransactionRequest, context) -> AppTransactionsResponse:
        user_token = self.ValidateToken(request.token)
        response = AppTransactionsResponse()

        if user_token is not None:
            transactions = self.data_service.get_account_transaction_with_id(user_token.account_id, request.transaction_id)

            # TODO populate data

            response.transactions

        return response

    def validate_payment_intent(self, amount: int, recipient_account_id: int, user_token: Optional[UserToken]) -> bool:
        # Prevent non-positive integer amounts
        if amount > 0:
            # Prevent accounts from sending money to themselves
            if user_token and user_token.account_id != recipient_account_id:
                # Prevent accounts from sending money to non-existent accounts
                if self.data_service.account_by_id_exists(recipient_account_id):
                    return True

        return False

    def EvaluatePaymentIntent(self, request: AppPaymentIntentRequest, context) -> EvaluatePaymentIntentResponse:
        user_token = self.ValidateToken(request.token)
        valid_payment_intent = False

        if user_token is not None:
            fees = 0
            valid_payment_intent = self.validate_payment_intent(request.amount, request.recipient_account_id, user_token)

            if valid_payment_intent:
                fees = calculate_fees(amount=request.amount)

        return EvaluatePaymentIntentResponse(valid_payment_intent=valid_payment_intent, fees=fees)

    def PostPaymentIntent(self, request: AppPaymentIntentRequest, context) -> AppAccountDetailsResponse:
        user_token = self.ValidateToken(request.token)
        response = AppAccountDetailsResponse()
        
        transaction: Optional[TransactionModel] = None

        if user_token is not None:
            fees = 0
            valid_payment_intent = self.validate_payment_intent(request.amount, request.recipient_account_id, user_token)
    
            if valid_payment_intent:
                fees = calculate_fees(amount=request.amount)

                transaction = self.data_service.post_payment_intent(
                    user_token.account_id,
                    request.recipient_account_id,
                    fees,
                    request.amount,
                    request.message
                )

                response.transaction = transaction

        return response
