from typing import Optional


class FeeTier:
    fee_cap: int
    name: str
    decimal_percent: float
    range_from: int
    range_to: Optional[int]

    def __init__(self, fee_cap, name, decimal_percent, range_from, range_to=None):
        self.range_from = range_from
        self.range_to = range_to
        self.fee_cap = fee_cap
        self.name = name
        self.decimal_percent = decimal_percent

    def fee(self, amount: int) -> int:
        is_number_in_range = False

        if amount >= self.range_from and self.range_to is None:
            is_number_in_range = True
        elif amount >= self.range_from and amount <= self.range_to:
            is_number_in_range = True

        if is_number_in_range:
            percent_fee_amount = amount * self.decimal_percent
            
            if percent_fee_amount > self.fee_cap:
                return self.fee_cap
            else:
                return percent_fee_amount
        else:
            return -1

def inputted_amount_to_cents(amount: float) -> int:
    return int(amount * 100)

def percent_to_decimal(amount: float) -> float:
    return amount / 100


TRANSFER_FEES: list[FeeTier] = [
    FeeTier(0, "Free Tier", 0, 0, inputted_amount_to_cents(2000)),
    FeeTier(inputted_amount_to_cents(20), "Entry Tier", percent_to_decimal(0.25), inputted_amount_to_cents(2000.01), inputted_amount_to_cents(10000)),
    FeeTier(inputted_amount_to_cents(25), "Mid Tier", percent_to_decimal(0.20), inputted_amount_to_cents(10000.01), inputted_amount_to_cents(20000)),
    FeeTier(inputted_amount_to_cents(40), "Upper-mid Tier", percent_to_decimal(0.125), inputted_amount_to_cents(20000.01), inputted_amount_to_cents(50000)),
    FeeTier(inputted_amount_to_cents(60), "High Tier", percent_to_decimal(0.08), inputted_amount_to_cents(50000.01), inputted_amount_to_cents(100000)),
    FeeTier(inputted_amount_to_cents(200), "Top Tier", percent_to_decimal(0.06), inputted_amount_to_cents(100000.01), None),
]

def calculate_fees(amount: int) -> int:
    FEE_NOT_APPLICABLE = -1

    for transfer_fee in TRANSFER_FEES:
        fee = transfer_fee.fee(amount)

        if fee == FEE_NOT_APPLICABLE:
            continue
        else:
            return fee
