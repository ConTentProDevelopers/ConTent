from django.contrib.auth.models import User
from django import forms
from .models import *


class CustomerRegisterForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'phone_number', 'email','password']
        exclude = ['email_validated', 'is_active','is_superuser']

class FieldOwnerRegisterForm(forms.ModelForm):

    class Meta:
        model = FieldOwner
        fields = ['company_name','company_NIP','company_REGON','company_postal_code','company_locality','company_address']
        exclude = ['account_validated']