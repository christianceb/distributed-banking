from typing import Optional

from models.Account import Account
from models.User import User


class SessionData:
    user_id: int
    account_id: int
    user: Optional[User]
    account: Optional[Account]
    token: str
