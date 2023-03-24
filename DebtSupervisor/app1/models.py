from django.db import models
from django.contrib.auth.models import User
import math
# Create your models here.

class Debtentry(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    currBalance = models.FloatField()
    TotalBalance = models.FloatField()
    Name = models.CharField(max_length=128)
    AprRate = models.FloatField()
    transactionDate = models.DateField()
   
    def getProgress(self):
        return math.ceil((self.currBalance/self.TotalBalance)*100)
