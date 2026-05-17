def int_cents_to_localised(cents: int) -> str:
    sign = '-' if cents < 0 else ''
    
    cents_abs = abs(int(cents))
    
    dollars, cents_part = divmod(cents_abs, 100)
    
    return f"{sign}${dollars}.{cents_part:02d}"
