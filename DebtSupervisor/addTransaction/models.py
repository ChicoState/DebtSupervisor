from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class expenseCategory(models.Model):
    category = models.CharField(max_length = 128)
    def __str__(self):
        return self.category

class expenseEntry(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transactionAmount = models.IntegerField()
    description = models.CharField(max_length=128)
    category = models.ForeignKey(expenseCategory,on_delete=models.CASCADE)
    transactionDate = models.DateField()

# Create your models here.
