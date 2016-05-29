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
    campsites = Campsite.objects.all()
    active = campsites[0]
    campsites=campsites[1:]
    context = {'campsites':campsites,'active':active}
    return render(request, 'index.html',context)


def indexpage(request):
    return render(request, 'indexpage.html')


def addfield(request):
    return render(request, 'addfield.html')


def confirmation(request):
    return render(request, 'confirmation.html')


def newreservation(request):
    return render(request, 'new-reservation.html')


def newreservation2(request):
    return render(request, 'new-reservation2.html')


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
    if not request.POST:
        return render(request, 'login.html', {'state': state})
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = get_user(email=email, password=password)
    state = check_user_state(user)
    if state != 'correct':
        return render_to_response('login.html', {'state': state, 'email': email}, RequestContext(request))
    if user_is_field_owner(user):
        return userownerstart(request,user.id)
    if user_is_customer(user):
        return userclientstart(request,user.id)

def get_user(email, password):
    try:
        user = authenticate(username=email, password=password)
        # hacking begins here :<
        if password!=MyUser.objects.get(email=email).password:
            user=None
    except:
        user = None
    return user

def check_user_state(user):
    if user is None:
            return "Your username and/or password were incorrect."
    if not user.is_active:
            return "Your account is not active, please contact the site admin."
    if not (user_is_field_owner(user) or user_is_customer(user)):
            return "User is not customer nor fieldOwner"
    return 'correct'

def user_is_customer(user):
    try:
        user.customer
    except:
        return False
    return True

def user_is_field_owner(user):
    try:
        user.fieldowner
    except:
        return False
    return True

def myreservations(request):
    return render(request, 'myreservations.html')


def postsearch(request):
    search_text = request.GET.get('search')
    keywords = [keyword.lower() for keyword in str(search_text).split()]
    matched_campsites=[]
    for campsite in Campsite.objects.all():
        if keywords_match_campsite_name_or_locality(keywords,campsite):
            matched_campsites.append(campsite)
    context = {'matched_campsites':matched_campsites}
    return render(request, 'postsearch.html',context)

def keywords_match_campsite_name_or_locality(keywords,campsite):
    keywords_found_in_name = any(keyword in campsite.field_name.lower() for keyword in keywords)
    keywords_found_in_locality = any(keyword in campsite.field_locality.lower() for keyword in keywords)
    return keywords_found_in_name or keywords_found_in_locality


def static_page(request):
    return render(request, 'static_page.html')


def user(request):
    return render(request, 'user.html')


def user_changepassword(request):
    return render(request, 'user_changepassword.html')

def userownerstart(request,user_id):
    field_owner = MyUser.objects.get(id = user_id).fieldowner
    context = {'campsites':Campsite.objects.filter(field_owner=field_owner)}
    return render(request, 'user-owner-startpage-myfields.html',context)

def userclientstart(request,user_id):
    client = MyUser.objects.get(id = user_id).customer
    context = {'first_name':client.user.first_name,
               'last_name':client.user.last_name,
               'phone_number':client.user.phone_number}
    return render(request, 'user-client-startpage.html',context)

def userowneraddfield(request):
    return render(request, 'user-owner-fieldedit.html')


def register(request):
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
