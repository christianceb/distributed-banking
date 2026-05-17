from typing import Optional


class UserToken:
    user_id = None
    account_id = None
    token = None

    def __init__(self):
        pass

class UserTokenService:
    user_tokens: list[UserToken] = []

    def __init__(self):
        pass

    def GenerateUserToken(self, user_id: int, account_id: int, entropy: list[str]) -> UserToken:
        draft_token = ";".join(entropy);

        user_token = self.FindToken(draft_token)

        if user_token is None:
            user_token = UserToken()

            user_token.user_id = user_id
            user_token.account_id = account_id
            user_token.token = draft_token

            self.user_tokens.append(user_token)
        
        return user_token

    def FindToken(self, token: str) -> Optional[UserToken]:
        user_token = None

        for user_token in self.user_tokens:
            if user_token.token == token:
                user_token.token = token
                break

        return user_token
