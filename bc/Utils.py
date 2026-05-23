from Models import PublicTransactionModel
from CurrencyHelper import int_cents_to_localised


def amount_no_fee(transaction: PublicTransactionModel) -> int:
    return transaction.amount - transaction.fees

def render_txn_amount(transaction: PublicTransactionModel, account_id: int) -> int:
    localised = int_cents_to_localised(amount_no_fee(transaction))

    if transaction.recipient_account_id == account_id:
        localised = "+" + localised
    else:
        localised = "-" + localised

    return localised
