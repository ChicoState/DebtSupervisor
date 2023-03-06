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
    currBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Current Balance"}))
    TotalBalance = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"Total Available"}))
    Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Name"}))
    AprRate = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':"APR Rate"}))
    transactionDate = forms.DateField(widget=forms.DateInput(attrs={'placeholder':"MM-DD-YYYY"}))

    class Meta():
        model = Debtentry
        fields = ('currBalance','TotalBalance','Name','AprRate','transactionDate')
