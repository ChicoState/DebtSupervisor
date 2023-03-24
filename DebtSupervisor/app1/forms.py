from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, ModelForm, Textarea
from app1.models import Debtentry

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
    help_texts = {
        'username': None
    }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class debtForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Nickname"}))
    currBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Current Balance"}))
    TotalBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Total Balance"}))
    apr = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Annual Percentage Rate"}))
    minPayment = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Minimum Payement"}))
    dueDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta():
        model = Debtentry
        fields = ('type', 'name','currBalance', 'TotalBalance','apr','minPayment','dueDate')
        widget = {
            'type' : forms.Select(choices=Debtentry.DEBT_TYPES),
        }
