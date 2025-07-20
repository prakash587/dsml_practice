def calculate_tax(income, tax_rate=0.15):
    """
    Calculate tax based on income and optional tax rate.
    Default tax rate = 15%
    """
    if income < 0:
        raise ValueError("Income cannot be negative.")
    return income * tax_rate
