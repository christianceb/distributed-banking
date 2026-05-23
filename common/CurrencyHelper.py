import locale


locale.setlocale(locale.LC_ALL, 'C')

def int_cents_to_localised(cents: int) -> str:
    return '${:,.2f}'.format(cents / 100)

def inputted_amount_to_cents(amount: float) -> int:
    return int(amount * 100)
