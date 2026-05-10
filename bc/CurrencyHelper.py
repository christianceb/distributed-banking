def int_cents_to_localised(cents: int) -> str:
    return "$" + str(cents / 100)
