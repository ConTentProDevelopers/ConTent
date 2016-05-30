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
from datetime import datetime
from random import randrange
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

    arrival = request.POST.get("arrival")
    departure = request.POST.get("departure")
    campsite_id = request.POST.get("campsite_id")
    campsite = get_object_or_404(Campsite,id=campsite_id)
    places_of_campsite = PlaceType.objects.filter(campsite=campsite)
    for place in places_of_campsite:
        place.reserved_spaces = request.POST.get(str(place.id))
    buyer = MyUser.objects.get(id=request.user.id)
    price = sum([(float(place.price) * float(place.reserved_spaces)) for place in places_of_campsite])
    context={"campsite":campsite,"places_of_campsite":places_of_campsite,"arrival":arrival,
             "departure":departure,"buyer":buyer,"price":price}
    return render(request, 'confirmation.html',RequestContext(request,context))

def confirm_reservation(request):
    arrival = request.POST.get("arrival")
    print (arrival)
    arrival = "{2}-{0}-{1}".format(*arrival.split("/"))
    departure = request.POST.get("departure")
    departure = "{2}-{0}-{1}".format(*departure.split("/"))
    campsite_id = request.POST.get("campsite_id")
    campsite = get_object_or_404(Campsite,id=campsite_id)
    buyer = MyUser.objects.get(id=request.user.id)
    field_owner = campsite.field_owner
    reservation = Reservation.objects.create(arrival_date=arrival,departure_date=departure,customer=buyer.customer,fieldOwner=field_owner,status="pending")
    reservation.save()
    places_of_campsite = PlaceType.objects.filter(campsite=campsite)
    for place_type in places_of_campsite:
        reserved_spaces = int(request.POST.get(str(place_type.id)))
        for i in range(reserved_spaces):
            o=Place.objects.create(placeType=place_type,reservation = reservation)
            o.save()


    return redirect("/user")

@login_required(login_url="/login/")
def newreservation(request,id):
    campsite = get_object_or_404(Campsite,id=id)
    context = {"campsite":campsite}
    return render(request, 'new-reservation.html',RequestContext(request,context))

@login_required(login_url="/login/")
def newreservation2(request):
    arrival = request.POST.get("arrival_date")
    departure = request.POST.get("departure_date")
    arrival_date = datetime.strptime(request.POST.get("arrival_date"),"%m/%d/%Y")
    departure_date = datetime.strptime(request.POST.get("departure_date"),"%m/%d/%Y")
    campsite_id = request.POST.get("campsite_id")
    campsite = get_object_or_404(Campsite,id=campsite_id)
    if departure_date < arrival_date:
        context = {"message":"wybrano złą date","campsite":campsite}
        return render(request,"new-reservation.html",RequestContext(request,context))
    places_of_campsite = PlaceType.objects.filter(campsite=campsite)
    for place in places_of_campsite:
        if place.number_of_places < place.limit_of_places:
            place.limit_of_places = range(place.number_of_places+1)
        else:
            place.limit_of_places = range(place.limit_of_places+1)
    context = {"arrival":arrival,"departure":departure,"places_of_campsite":places_of_campsite,"campsite_id":campsite_id}
    return render(request, 'new-reservation2.html',RequestContext(request,context))


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
    if request.GET.get("next"):
        print ("tuuuutaj")
        return redirect(request.GET.get("next"))
    if user.is_field_owner():
        return userownerstart(request)
    if user.is_customer():
        return userclientstart(request)

def get_user(email, password):
    # hacking begins here :<
    try:
        user = authenticate(username = email,password=password)
        if user.password == "password":
            if password!="password": #kacking fixtures
                user=None
        else:
            if not user.check_password(password): #haxing quickfix panic much regret
                user = None
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
    user = MyUser.objects.get(id=request.user.id)
    reservations = Reservation.objects.filter(customer = user.customer)
    for r in reservations:
        r.campsite = Campsite.objects.get(id = randrange(9) )
    print (len(reservations))
    context = {"reservations":reservations}
    return render(request, 'user-client-myreservations.html',context)

def single_reservation(request):
    return render(request, 'user-client-reservation.html')

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
    if request.user.is_customer():
        return userclientstart(request)
    return userownerstart(request)


def user_editlogin(request):
    if not request.POST:
        return render(request, 'user-client-editlogin.html',RequestContext(request))
    password = request.POST.get("password")
    password_confirmation = request.POST.get("password_confirmation")
    if password != password_confirmation:
        return render(request, 'user-client-editlogin.html',RequestContext(request))
    request.user.email = request.POST.get("email")
    request.user.set_password(request.POST.get("password"))
    request.user.save()
    return user(request)



def user_editprofile(request):
    if not request.POST:
        return render(request, 'user-client-editprofile.html',RequestContext(request))
    request.user.first_name = request.POST.get("first_name")
    request.user.last_name = request.POST.get("last_name")
    request.user.phone_number = request.POST.get("phone_number")
    request.user.save()
    return user(request)



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


def userownereditlogin(request):
    return render(request, 'user-owner-editlogin.html')


def userownereditprofile(request):
    return render(request, 'user-owner-editprofile.html')


def userownermyprofile(request):
    return render(request, 'user-owner-myprofile.html')


def userownerfieldedit(request):
    return render(request, 'user-owner-fieldedit.html')


def userownerfielinfo(request):
    return render(request, 'user-owner-fieldinfo.html')


def register(request):
    if(request.POST):
        customerForm = CustomerRegisterForm(request.POST)
        owner = request.POST.get('owner',None)
        if customerForm.is_valid():
            newUser = customerForm.save(commit=False)
            password = customerForm.cleaned_data.get('password')
            newUser.set_password(password)
            newUser.save()

            if owner is None:
                newCustomer = Customer()
                newCustomer.user = newUser
                newCustomer.save()
                return HttpResponseRedirect('/')
            else:
                newFieldOwner = FieldOwner()
                newFieldOwner.user = newUser
                newFieldOwner.save()
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
