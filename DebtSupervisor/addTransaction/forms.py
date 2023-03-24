from django import forms
from addTransaction.models import expenseEntry, expenseCategory
from dataclasses import fields
from tkinter import Widget
from django.core import validators
from django.forms import CharField, ModelForm, Textarea
from django.contrib.auth.models import User

class expenseEntryForm(forms.ModelForm):
    transactionAmount = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':"Amount"}))
    description = forms.CharField(widget=forms.TextInput(attrs={'size':'80','placeholder':"Description"}))
    category = forms.ModelChoiceField(queryset=expenseCategory.objects.all())
    transactionDate = forms.DateField(widget=forms.DateInput(attrs={'placeholder':"MM-DD-YYYY"}))
    class Meta():
        model= expenseEntry
        fields = ('transactionAmount','description','category','transactionDate')