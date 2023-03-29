from django.db import models
from django.contrib.auth.models import User
import math
from app1.utils import calculate_payoff
# Create your models here.

class Debtentry(models.Model):
    CREDIT_CARD = 'Credit Card'
    AUTO_LOAN = 'Auto Loan'
    PERSONAL_LOAN = 'Personal Loan'
    STUDENT_LOAN = 'Student Loan'
    MORTGAGE = 'Mortgage'
    MEDICAL_LOAN = 'Medical Loan'
    TAXES = 'Taxes'
    OTHER = 'Other'

    DEBT_TYPES = [
        (CREDIT_CARD, 'Credit Card'),
        (AUTO_LOAN, 'Auto Loan'),
        (PERSONAL_LOAN, 'Personal Loan'),
        (STUDENT_LOAN, 'Student Loan'),
        (MORTGAGE, 'Mortgage'),
        (MEDICAL_LOAN, 'Medical Loan'),
        (TAXES, 'Taxes'),
        (OTHER, 'Other'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=DEBT_TYPES)
    name = models.CharField(max_length=128)
    currBalance = models.FloatField()
    TotalBalance = models.FloatField()
    apr = models.FloatField()
    minPayment = models.FloatField()
    dueDate = models.DateField()

    def getProgress(self):
        return math.ceil((self.currBalance/self.TotalBalance)*100)
    
    @property
    def months_to_payoff(self):
        months,_ = calculate_payoff(self.currBalance, self.minPayment, self.apr)
        return months
    
    @property
    def total_interest(self):
        _,total_interest = calculate_payoff(self.currBalance, self.minPayment, self.apr)
        return round(total_interest, 2)
