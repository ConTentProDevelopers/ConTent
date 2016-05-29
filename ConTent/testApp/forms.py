from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import *


class CustomerRegisterForm(forms.ModelForm):
    owner = forms.BooleanField(label='Konto właściciela',required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','style' : 'width:50%'}),label='Imię',error_messages={'required': 'To pole jest wymagane!'})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','style' : 'width:50%'}),label='Nazwisko',error_messages={'required': 'To pole jest wymagane!'})
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','style' : 'width:50%'}),label='Telefon',error_messages={'required': 'To pole jest wymagane!'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control','style' : 'width:50%'}),label='Hasło',error_messages={'required': 'To pole jest wymagane!'})
    email = forms.CharField(widget=forms.TextInput(attrs={'style' : 'width:50%','class' : 'form-control'}),label='E-mail',error_messages={'unique': 'Ten email istnieje w bazie!'})
    class Meta:
        model = MyUser
        fields = ['owner','first_name', 'last_name', 'phone_number', 'email','password']
        exclude = ['email_validated', 'is_active','is_superuser']


class FieldOwnerRegisterForm(forms.ModelForm):

    class Meta:
        model = FieldOwner
        fields = ['company_name','company_NIP','company_REGON','company_postal_code','company_locality','company_address']
        exclude = ['account_validated']

class ReservationForm(forms.ModelForm):
    arrival_date = forms.DateField(label="Przyjazd")
    departure_date = forms.DateField(label="Odjazd")
    class Meta:
        model = Reservation
        fields=['arrival_date','departure_date']