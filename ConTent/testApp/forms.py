from django.contrib.auth.models import User
from django import forms
from .models import *


class CustomerRegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='Imię',error_messages={'required': 'To pole jest wymagane!'})
    last_name = forms.CharField(label='Nazwisko',error_messages={'required': 'To pole jest wymagane!'})
    phone_number = forms.CharField(label='Telefon',error_messages={'required': 'To pole jest wymagane!'})
    password = forms.CharField(label='Hasło',widget=forms.PasswordInput,error_messages={'required': 'To pole jest wymagane!'})
    email = forms.CharField(label='E-mail',error_messages={'unique': 'Ten email istnieje w bazie!'})
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'phone_number', 'email','password']
        exclude = ['email_validated', 'is_active','is_superuser']


class FieldOwnerRegisterForm(forms.ModelForm):

    class Meta:
        model = FieldOwner
        fields = ['company_name','company_NIP','company_REGON','company_postal_code','company_locality','company_address']
        exclude = ['account_validated']
