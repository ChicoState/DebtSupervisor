import math

def calculate_payoff(currbalance, minpayment, apr):
    apr = apr / 100
    n = -(math.log(1 - (apr/12) * currbalance / minpayment)) / (math.log(1 + apr/12))
    n = math.ceil(n) # round up to nearest month
    
    total_interest = 0
    remaining_balance = currbalance
    
    for _ in range(n):
        interest = remaining_balance * apr / 12
        principal = minpayment - interest
        remaining_balance -= principal
        total_interest += interest
        
    return n, total_interest