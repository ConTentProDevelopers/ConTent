from django.shortcuts import render
from django.core.context_processors import csrf
# Create your views here.
from .models import *
from .forms import *

def index(request):
    return render(request, 'index.html')


# 14.04.2016 TG
# Narazie działa to w ten sposób jeżeli dane dla klienta bedą poprawne to sprawdza czy dane
# wlasciciela sa poprawne jezeli sa tworzy wlascicela jezeli nie to klienta a jesli klient jest niepoprawny
# to nic nie robi

# Trzeba dodac skrypt ktory po wybraniu opcji klient/wlasciciel pokazuje opdpowiednie pola
# jezeli ktos chce przetestowac np dla klienta to trzeba wypelnic dane dla kilenta w sekcji wlasiciela rowniez

# w modelach trzeba poprawic kod pocztowy na 6 znakow bo nie dziala 00-000

def register(request):
    c_form = CustomerRegisterForm
    fo_form = FieldOwnerRegisterForm
    if(request.POST):
        customerForm = CustomerRegisterForm(request.POST)
        fieldOwnerForm = FieldOwnerRegisterForm(request.POST)
        if customerForm.is_valid():
            if fieldOwnerForm.is_valid():
                # tworzę nowego użytkownika z formularza i zapisuję
                newUser = customerForm.save(commit=False)
                password = customerForm.cleaned_data.get('password')
                newUser.set_password(password)
                newUser.save()

                # towrzę nowego wlascicela i przypisuje mu nowego użytkownika
                newFieldOwner = fieldOwnerForm.save(commit=False)
                newFieldOwner.user = newUser
                newFieldOwner.save()
                return render(request, 'register.html', {'form': fo_form})
            else:
                # tworzę nowego użytkownika z formularza i zapisuję
                newUser = customerForm.save(commit=False)
                password = customerForm.cleaned_data.get('password')
                newUser.set_password(password)
                newUser.save()

                # towrzę nowego klienta i przypisuje mu nowego użytkownika
                newCustomer = Customer()
                newCustomer.user = newUser
                newCustomer.save()
            return render(request, 'register.html', {'form': c_form})
    return render(request, 'register.html', {'form': c_form})



def indexpage(request):
    return render(request, 'indexpage.html')


def addfield(request):
    return render(request, 'addfield.html')


def confirmation(request):
    return render(request, 'confirmation.html')


def error404(request):
    return render(request, 'error404.html')


def fields(request):
    return render(request, 'fields.html')


def fieldsite(request):
    return render(request, 'fieldsite.html')


def footer(request):
    return render(request, 'footer.html')


def forgotemail(request):
    return render(request, 'forgotemail.html')


def forgotpassword(request):
    return render(request, 'forgotpassword.html')


def header(request):
    return render(request, 'header.html')


def login(request):
    return render(request, 'login.html')


def myreservations(request):
    return render(request, 'myreservations.html')


def postsearch(request):
    return render(request, 'postsearch.html')




def static(request):
    return render(request, 'static.html')


def user(request):
    return render(request, 'user.html')


def user_changepassword(request):
    return render(request, 'user_changepassword.html')

