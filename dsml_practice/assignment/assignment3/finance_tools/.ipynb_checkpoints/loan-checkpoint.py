def calculate_emi(principal, rate, years):
    """
    Calculate EMI using formula:
    EMI = [P × R × (1 + R)^N] / [(1 + R)^N – 1]
    where:
      P = loan amount,
      R = monthly interest rate,
      N = total months
    """
    if principal <= 0 or rate <= 0 or years <= 0:
        raise ValueError("Values must be greater than zero.")

    monthly_rate = rate / (12 * 100)  # Annual to monthly
    months = years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return round(emi, 2)
