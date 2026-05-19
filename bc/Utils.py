from Models import Transaction
from CurrencyHelper import int_cents_to_localised


def amount_no_fee(transaction: Transaction) -> int:
    return transaction.amount - transaction.fees

def render_txn_amount(transaction: Transaction, account_id: int) -> int:
    localised = int_cents_to_localised(amount_no_fee(transaction))

    if transaction.destination_account_id == account_id:
        localised = "+" + localised
    else:
        localised = "-" + localised

    return localised
