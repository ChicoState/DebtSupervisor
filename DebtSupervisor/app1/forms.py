from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, ModelForm, Textarea
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from app1.models import Debtentry
from app1.utils import calculate_payoff

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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class debtForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Nickname"}))
    currBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Current Balance"}))
    TotalBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Total Balance"}))
    minPayment = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Minimum Payment"}))
    apr = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Annual Percentage Rate"}))
    dueDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta():
        model = Debtentry
        fields = ('type','name','currBalance','TotalBalance','apr', 'minPayment','dueDate')
        widget = {
            'type' : forms.Select(choices=Debtentry.DEBT_TYPES),
        }
