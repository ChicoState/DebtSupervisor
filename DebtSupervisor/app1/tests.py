from django.test import TestCase
from django.contrib.auth.models import User
from app1.models import Debtentry
from .forms import debtForm

# Create your tests here.
#Test model of debt entry
class DebtentryTEST(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.debt = Debtentry.objects.create(
            user=self.user,
            type =Debtentry.CREDIT_CARD,
            name = "Discover Card",
            currBalance = 1000,
            TotalBalance = 2000,
            apr = 5,
            minPayment = 50,
            dueDate = "2023-05-12"
        )

    def test_getProgress(self):
        self.assertEqual(self.debt.getProgress(), 50)

    def test_months_to_payoff(self):
        self.assertEqual(self.debt.months_to_payoff, 20)
    def test_total_interest(self):
        self.assertEqual(round(self.debt.total_interest), 46)

#Test form of debt entry
class debtFormTEST(TestCase):
    def test_valid(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 5,
            'minPayment': 50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertTrue(form.is_valid())

    def test_currBalance(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': -1000,
            'TotalBalance': 2000,
            'apr': 5,
            'minPayment': 50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['currBalance'], ["Balance cannot be negative"])
   
    def test_TotalBalance(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': -2000,
            'apr': 5,
            'minPayment': 50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['TotalBalance'], ["Balance cannot be negative"])
    
    def test_curr_greater_than_total(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 2000,
            'TotalBalance': 1000,
            'apr': 5,
            'minPayment': 50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['TotalBalance'], ['Total balance cannot be less than current balance.'])

    def test_apr(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': -5,
            'minPayment': 50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['apr'], ["APR must be between 0 and 100"])
    
    def test_payments_greater_than_accum_intrest(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 39,
            'minPayment': 20,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['minPayment'], ['Minimum payment must be greater than accumulated interest.'])
