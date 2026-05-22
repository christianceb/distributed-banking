from Models import TransactionModel
from CurrencyHelper import int_cents_to_localised


def amount_no_fee(transaction: TransactionModel) -> int:
    return transaction.amount - transaction.fees

def render_txn_amount(transaction: TransactionModel, account_id: int) -> int:
    localised = int_cents_to_localised(amount_no_fee(transaction))

    if transaction.recipient_account_id == account_id:
        localised = "+" + localised
    else:
        localised = "-" + localised

    return localised
