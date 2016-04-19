from django.shortcuts import render

# Create your views here.


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


def login(request):
    return render(request, 'login.html')


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

