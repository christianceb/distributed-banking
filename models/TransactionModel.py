class TransactionModel:
    id: int
    source_account_id: int
    recipient_account_id: int
    amount: int
    message: str
    status: str
    fees: int
    kind: str
    tries: int # Omitted outside BDB
    timestamp: int
    updated_at: int
