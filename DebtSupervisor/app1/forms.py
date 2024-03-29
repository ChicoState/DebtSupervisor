from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, ModelForm, Textarea
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from app1.models import Debtentry
from app1.utils import calculate_payoff,validateBalances,validateAPR
from app1.models import UserProfile

class UserProfileForm(forms.ModelForm):
    profilePic = forms.ImageField(label="Profile Picture")
    class Meta:
        model = UserProfile
        fields = ('profilePic', )

# validators for password
def validate_password(value):
    if len(value) < 8:
        raise ValidationError(
            _("Password must be at least 8 characters long."),
            code='password_too_short'
        )
    if not any(char.isdigit() for char in value):
        raise ValidationError(
            _("Password must contain at least one digit."),
            code='password_no_digit'
        )
    if not any(char.isalpha() for char in value):
        raise ValidationError(
            _("Password must contain at least one letter."),
            code='password_no_letter'
        )

class CustomPasswordValidator:
    def validate(self, password, user=None):
        validate_password(password)

    def get_help_text(self):
        return _("Your password must be at least 8 characters long, contain at least one letter, and at least one digit.")

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not username or not password:
            self.add_error('username', 'Please enter a valid username and password.')
    '''
    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password:
            self.add_error('username', 'Please enter a valid username and password.')
            return False
        return True
    '''
    help_texts = {
        'username': None
    }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class debtForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Nickname"}))
    currBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Current Balance"}),validators=[validateBalances])
    TotalBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Total Balance"}),validators=[validateBalances])
    minPayment = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Minimum Payment"}))
    apr = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Annual Percentage Rate"}),validators=[validateAPR])
    dueDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta():
        model = Debtentry
        fields = ('type','name','currBalance','TotalBalance','apr', 'minPayment','dueDate')
        widget = {
            'type' : forms.Select(choices=Debtentry.DEBT_TYPES),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        currBalance = cleaned_data.get('currBalance')
        TotalBalance = cleaned_data.get('TotalBalance')
        apr = cleaned_data.get('apr')
        minPayment = cleaned_data.get('minPayment')
        if currBalance is not None and TotalBalance is not None and currBalance > TotalBalance:
            self.add_error('currBalance', 'Current balance cannot be greater than total balance.')
            self.add_error('TotalBalance', 'Total balance cannot be less than current balance.')

        if apr is not None and minPayment is not None and currBalance is not None:
            interest_rate = (apr / 100) 
            year_paid = minPayment * 12
            year_interest_paid = currBalance * interest_rate
            if year_paid < year_interest_paid:
                self.add_error('minPayment', 'Minimum payment must be greater than accumulated interest.')
       
    #affordability validators
class Affordability(forms.Form):
    monthly_income = forms.FloatField(required=True, min_value=0)
    monthly_expenses = forms.FloatField(required=True, min_value=0)
    monthly_savings = forms.FloatField(required=True, min_value=0)
    cost_of_purchase = forms.FloatField(required=True, min_value=0)
    
    def clean(self):
        cleaned_data = super().clean()
        monthly_income = cleaned_data.get("monthly_income")
        monthly_expenses = cleaned_data.get("monthly_expenses")
        monthly_savings = cleaned_data.get("monthly_savings")
        cost_of_purchase = cleaned_data.get("cost_of_purchase")
        
        if cost_of_purchase is not None:
            if cost_of_purchase < 0:
                self.add_error(
                    "cost_of_purchase", "Cost of purchase cannot be negative."
                )
        else:
            self.add_error(
                "cost_of_purchase", "Cost of purchase cannot be empty or negative."
            )
        
        if monthly_income is not None and monthly_expenses is not None and monthly_savings is not None:
                if monthly_savings > monthly_income:
                    self.add_error(
                        "monthly_savings", "Monthly savings cannot be greater than monthly income."
                    )
                if monthly_expenses > monthly_income:
                    self.add_error(
                        "monthly_expenses", "Monthly expenses cannot be greater than monthly income."
                    )
                if monthly_savings > (monthly_income - monthly_expenses):
                    self.add_error(
                        "monthly_savings", "Monthly savings cannot be greater than the difference between monthly income and monthly expenses."
                    )
                if monthly_income < (monthly_expenses + monthly_savings):
                    self.add_error(
                        "monthly_income", "Monthly income must be greater than the sum of monthly expenses and monthly savings."
                    )
                if monthly_income < 0 :
                    self.add_error(
                        "monthly_income", "Monthly income cannot be negative."
                    )
                if monthly_expenses < 0 :
                    self.add_error(
                        "monthly_expenses", "Monthly expenses cannot be negative."
                    )
                if monthly_savings < 0 :
                    self.add_error(
                        "monthly_savings", "Monthly savings cannot be negative."
                    )

                    