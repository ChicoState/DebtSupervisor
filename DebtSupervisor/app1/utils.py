import math
from django.core.exceptions import ValidationError

def calculate_payoff(currbalance, minpayment, apr):
    total_interest = 0
    n = 0
    
    if apr != 0:
        #calculate number of months to pay off
         apr = apr / 100
         n = -(math.log(1 - (apr/12) * currbalance / minpayment)) / (math.log(1 + apr/12))
         n = math.ceil(n) # round up to nearest month
         
         remaining_balance = currbalance
             
    for _ in range(n):
        #calculate interest and principal when APR not 0
        interest = remaining_balance * apr / 12
        principal = minpayment - interest
        remaining_balance -= principal
        total_interest += interest
            
    else :         
        #rounds up to nearest month
        n = math.ceil(currbalance / minpayment)           
    
    return n, total_interest

def validateBalances(balance):
    if balance < 0 :
        raise ValidationError("Balance cannot be negative")
    
def validateAPR(apr):
    if apr < 0.0 or apr > 100.0:
        raise ValidationError("APR must be between 0 and 100")

    