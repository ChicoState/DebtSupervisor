from django.test import TestCase,Client
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from app1.models import Debtentry,debt_Strategies
from django.urls import reverse
from .forms import debtForm
from .forms import Affordability

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
    
    def test_zero_apr(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 0,
            'minPayment': 50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertTrue(form.is_valid())
        
    def test_hundred_apr(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 100,
            'minPayment': 500,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertTrue(form.is_valid())
        
    def test_zero_min_payment(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 5,
            'minPayment': 0,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['minPayment'], ['Minimum payment must be greater than accumulated interest.'])
        
    def test_negative_min_payment(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 5,
            'minPayment': -50,
            'dueDate': "2023-05-12"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['minPayment'], ['Minimum payment must be greater than accumulated interest.'])
        
    def test_empty_form(self):
        form = debtForm(data={})
        self.assertFalse(form.is_valid())
        
    def test_invalid_date(self):
        form = {
            'name': 'Discover Card',
            'type': Debtentry.CREDIT_CARD,
            'currBalance': 1000,
            'TotalBalance': 2000,
            'apr': 5,
            'minPayment': 50,
            'dueDate': "12-13-2023"
        }
        form = debtForm(data=form)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dueDate'], ['Enter a valid date.'])
        
class CalculateAffordabilityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_caluclate_affordability(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': 2000,
            'cost_of_purchase': 500,
            'monthly_savings': 1000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)

    def test_negative_income(self):
        url = '/result/'
        post_data = {
            'monthly_income': -5000,
            'monthly_expenses': 2000,
            'cost_of_purchase': 500,
            'monthly_savings': 1000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'monthly_income', 'Ensure this value is greater than or equal to 0.')
        
    def test_negative_expense(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': -2000,
            'cost_of_purchase': 500,
            'monthly_savings': 1000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'monthly_expenses', 'Ensure this value is greater than or equal to 0.')
        
    def test_negative_savings(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': 2000,
            'cost_of_purchase': 500,
            'monthly_savings': -1000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'monthly_savings', 'Ensure this value is greater than or equal to 0.')
        
    def test_negative_purchase(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': 2000,
            'cost_of_purchase': -1100,
            'monthly_savings': 1000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'cost_of_purchase', ['Ensure this value is greater than or equal to 0.', 'Cost of purchase cannot be empty or negative.'])
        
    def test_expandsav_more_than_income(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': 2000,
            'cost_of_purchase': 500,
            'monthly_savings': 4000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'monthly_income', 'Monthly income must be greater than the sum of monthly expenses and monthly savings.')
    
    def test_expense_more_than_income(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': 6000,
            'cost_of_purchase': 500,
            'monthly_savings': 1000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'monthly_income', 'Monthly income must be greater than the sum of monthly expenses and monthly savings.')
   
    def test_savings_more_than_everything(self):
        url = '/result/'
        post_data = {
            'monthly_income': 5000,
            'monthly_expenses': 2000,
            'cost_of_purchase': 500,
            'monthly_savings': 4000
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'monthly_savings', 'Monthly savings cannot be greater than the difference between monthly income and monthly expenses.')

class HomepageTestCase(TestCase):
    def setUp(self):
        # Create a user and some debt entries
        self.user = User.objects.create_user(username='testuser', password='testpass')
        Debtentry.objects.create(user=self.user, type=Debtentry.CREDIT_CARD, currBalance=100, TotalBalance=1000, dueDate=date.today(),apr= 5,minPayment = 35)
        Debtentry.objects.create(user=self.user, type=Debtentry.AUTO_LOAN, currBalance=500, TotalBalance = 2000,dueDate=date.today()+relativedelta(months=+1),apr = 8,minPayment = 55)

    def test_with_debt_entries(self):
        client = Client()
        client.force_login(self.user)
        response = client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credit Card")
        self.assertContains(response, "Auto Loan")
    
    def test_without_debt_entries(self):
        client = Client()
        client.force_login(self.user)
        Debtentry.objects.filter(user=self.user).delete()
        response = client.get('/home/')
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,"Credit Card")
        self.assertNotContains(response,"Auto Loan")

class DebtStratpageTestCase(TestCase):
    def setUp(self):
        self.snowflake = debt_Strategies.objects.create(name="Snowball Method", description="Pay off the smallest debt first, then use the money you would have used to pay off the smallest debt to pay off the next smallest debt, and so on.", url="https://www.debt.org/advice/debt-snowball-method-how-it-works/")
        self.avalanche = debt_Strategies.objects.create(name="Avalanche Method", description="Prioritize and pay off high-interest debt first, then use the freed-up funds to pay off other debts in descending order of interest rates.", url="https://www.debt.org/advice/debt-avalanche/")
        self.consolidation = debt_Strategies.objects.create(name="Debt Consolidation", description="Learn more ways to pay off debts", url="https://www.debt.org/consolidation/")
    
    def test_debt_strat_page(self):
        response = self.client.get('/debtstrategies/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response, self.snowflake.name)
        self.assertContains(response, self.snowflake.description)
        self.assertContains(response, self.snowflake.url)
        self.assertContains(response, self.avalanche.name)
        self.assertContains(response, self.avalanche.description)
        self.assertContains(response, self.avalanche.url)
        self.assertContains(response, self.consolidation.name)
        self.assertContains(response, self.consolidation.description)
        self.assertContains(response, self.consolidation.url)


class AddDebtpageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.debt_data = {
            "type": Debtentry.CREDIT_CARD,
            "name": "Test Card",
            "currBalance": 1000,
            "TotalBalance": 2000,
            "apr": 12.00,
            "minPayment": 25.00,
            "dueDate": date.today(),
        }

    def test_form_page(self):
        self.client.login(username = 'testuser',password = 'testpass')
        response = self.client.post(('/addDebt/'),self.debt_data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Debtentry.objects.count(), 1)






