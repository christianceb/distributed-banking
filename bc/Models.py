from typing import Optional

class PublicTransactionModel:
    id: int
    source_account_id: int
    recipient_account_id: int
    amount: int
    bas: str
    status: str
    fees: int
    kind: str
    timestamp: int
    updated_at: int

class User:
    id: int
    username: str
