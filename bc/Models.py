from typing import Optional

class Transaction:
    id: int
    source_account_id: int
    destination_account_id: int
    amount: int
    bas: str
    status: str
    fees: int
    kind: str
    tries: int
    timestamp: int
    updated_at: int

class User:
    id: int
    username: str

class Account:
    id: int
    current_balance: int
    available_balance: int

class SessionData:
    user_id: int
    account_id: int
    user: Optional[User]
    account: Optional[Account]
    token: str
