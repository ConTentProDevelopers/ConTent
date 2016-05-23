from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.core.context_processors import csrf
from django.template import RequestContext
# Create your views here.

User = get_user_model()


def index(request):
    campsites = Campsite.objects.all()
    active = campsites[0]
    campsites=campsites[1:]
    context = {'campsites':campsites,'active':active}
    return render(request, 'index.html',RequestContext(request,context))

def logout_method(request):
    logout(request)
    return redirect("/")

def indexpage(request):
    return render(request, 'indexpage.html')

def reservation(request):
    form = ReservationForm(request.POST or None)
    context = {'form':form}
    return render(request, 'reservation.html',RequestContext(request,context))

def addfield(request):
    return render(request, 'addfield.html')


def confirmation(request):
    arrival = request.POST.get("arrival_date")
    departure = request.POST.get("departure_date")
    customer = MyUser.objects.get(id=request.user.id).customer
    owner = MyUser.objects.get(id=request.user.id).fieldowner
    reservation = Reservation(arrival_date=arrival,departure_date=departure,
                              staus="pending",customer=customer,fieldOwner=owner)
    context={'reservation':reservation}
    return render(request, 'confirmation.html',RequestContext(request,context))

def confirm_reservation(request):
    arrival = request.POST.get("arrival_date")
    departure = request.POST.get("departure_date")
    customer = MyUser.objects.get(id=request.user.id).customer
    owner = MyUser.objects.get(id=request.user.id).fieldowner
    reservation = Reservation(arrival_date=arrival,departure_date=departure,
                              staus="pending",customer=customer,fieldOwner=owner)
    reservation.save()
    if request.user.is_customer():
        return redirect("/user-client-startpage")
    if request.user.is_field_owner():
         return redirect("/user-owner-startpage")

def error404(request):
    return render(request, 'error404.html')


def fields(request):
    return render(request, 'fields.html')


def fieldsite(request,id):
    campsite=get_object_or_404(Campsite,id=id)
    convenience = Convenience.objects.get(campsite=campsite)
    rating_integral = range(int(campsite.average_rating))
    rating_fractional = (campsite.average_rating%1)
    width_from_rating = 24*rating_fractional
    context={'campsite':campsite,'rating_integral':rating_integral,'star_width':width_from_rating,
             'convenience':convenience}
    return render(request, 'fieldsite.html',RequestContext(request,context))


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
    login(request,user)
    if user.is_field_owner():
        return userownerstart(request)
    if user.is_customer():
        return userclientstart(request)

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
    if not (user.is_field_owner() or user.is_customer()):
            return "User is not customer nor fieldOwner"
    return 'correct'


def myreservations(request):
    return render(request, 'user-client-myreservations.html')


def postsearch(request):
    search_text = request.GET.get('search')
    keywords = [keyword.lower() for keyword in str(search_text).split()]
    matched_campsites=[]
    for campsite in Campsite.objects.all():
        if keywords_match_campsite_name_or_locality(keywords,campsite):
            matched_campsites.append(campsite)
    context = {'matched_campsites':matched_campsites}
    return render(request, 'postsearch.html',RequestContext(request,context))

def keywords_match_campsite_name_or_locality(keywords,campsite):
    keywords_found_in_name = any(keyword in campsite.field_name.lower() for keyword in keywords)
    keywords_found_in_locality = any(keyword in campsite.field_locality.lower() for keyword in keywords)
    return keywords_found_in_name or keywords_found_in_locality


def static_page(request):
    return render(request, 'static_page.html')


def user(request):
    return render(request, 'user-client-startpage.html')


def user_editlogin(request):
    return render(request, 'user-client-editlogin.html')

def user_editprofile(request):
    return render(request, 'user-client-editprofile.html')

def userownerstart(request):
    field_owner = MyUser.objects.get(id = request.user.id).fieldowner
    context = {'campsites':Campsite.objects.filter(field_owner=field_owner)}
    return render(request, 'user-owner-startpage-myfields.html',RequestContext(request,context))

def userclientstart(request):
    client = MyUser.objects.get(id = request.user.id).customer
    context = {'first_name':client.user.first_name,
               'last_name':client.user.last_name,
               'phone_number':client.user.phone_number}
    return render(request, 'user-client-startpage.html',RequestContext(request,context))

def userowneraddfield(request):
    return render(request, 'user-owner-fieldedit.html')


def register(request):
    print("jolo")
    if(request.POST):
        customerForm = CustomerRegisterForm(request.POST)
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
