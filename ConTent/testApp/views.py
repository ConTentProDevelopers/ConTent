from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

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


def register(request):
    return render(request, 'register.html')


def static(request):
    return render(request, 'static.html')


def user(request):
    return render(request, 'user.html')


def user_changepassword(request):
    return render(request, 'user_changepassword.html')

