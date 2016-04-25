from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.core.context_processors import csrf
# Create your views here.

User = get_user_model()


def index(request):
    return render(request, 'index.html')


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


def login_user_form(request):
    state = "Please log in below..."
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

        return render_to_response('login.html', {'state': state, 'email': email}, RequestContext(request))
    else:
        return render(request, 'login.html', {'state': state})


def myreservations(request):
    return render(request, 'myreservations.html')


def postsearch(request):
    return render(request, 'postsearch.html')


def static_page(request):
    return render(request, 'static_page.html')


def user(request):
    return render(request, 'user.html')


def user_changepassword(request):
    return render(request, 'user_changepassword.html')

def userownerstart(request):
    return render(request, 'user-owner-startpage-myfields.html')

def userowneraddfield(request):
    return render(request, 'user-owner-fieldedit.html')

def register(request):
    print("jolo")
    if(request.POST):
        customerForm = CustomerRegisterForm(request.POST)
        print(customerForm)
        if customerForm.is_valid():
            # tworzę nowego użytkownika z formularza i zapisuję
            newUser = customerForm.save(commit=False)
            password = customerForm.cleaned_data.get('password')
            newUser.set_password(password)
            newUser.save()

            # towrzę nowego klienta i przypisuje mu nowego użytkownika
            newCustomer = Customer()
            newCustomer.user = newUser
            newCustomer.save()
            return HttpResponseRedirect('/')
    else:
        customerForm = CustomerRegisterForm()
    args = {}
    args.update(csrf(request))
    args['cform'] = customerForm
    return render_to_response('register.html', args)



# def register(request):
#     if(request.POST):
#         customerForm = CustomerRegisterForm(request.POST)
#         fieldOwnerForm = FieldOwnerRegisterForm(request.POST)
#         if customerForm.is_valid():
#             if fieldOwnerForm.is_valid():
#                 # tworzę nowego użytkownika z formularza i zapisuję
#                 newUser = customerForm.save(commit=False)
#                 password = customerForm.cleaned_data.get('password')
#                 newUser.set_password(password)
#                 newUser.save()
#
#                 # towrzę nowego wlascicela i przypisuje mu nowego użytkownika
#                 newFieldOwner = fieldOwnerForm.save(commit=False)
#                 newFieldOwner.user = newUser
#                 newFieldOwner.save()
#                 return HttpResponseRedirect('/testApp/index/')
#         else:
#             print('nie poprawny')
#             customerForm = CustomerRegisterForm()
#             fieldOwnerForm = FieldOwnerRegisterForm()
#         args = {}
#         args.update(csrf(request))
#         args['cform'] = customerForm
#         args['foform'] = fieldOwnerForm
#         print(args)
#         return render_to_response('register.html', args)
#     return render(request, 'register.html', {'foform': FieldOwnerRegisterForm,'cform': CustomerRegisterForm})
