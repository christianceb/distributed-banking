from models.PublicTransactionModel import PublicTransactionModel


def amount_no_fee(transaction: PublicTransactionModel) -> int:
    return transaction.amount - transaction.fees
