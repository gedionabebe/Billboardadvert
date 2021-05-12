from django.shortcuts import render, redirect
from decimal import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import forms
from .forms import rateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from billboards.forms import *
from django.contrib.auth import authenticate
from django.contrib import auth
from billboards.models import Billboard
from .forms import RegisterUserForm
from accounts.forms import *
from accounts.models import Administrator
from .models import *
import math

# the isAuthenticated list contains all of the authenticated users id
isAuthenticated = []


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in,
            login(request, user)
            # ie.redirect the user to another page
    else:
        form = UserCreationForm()
    return render(request, 'accounts/registration.html', {'form': form})


# the bottom registration method is functional.
def registrationtest(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            Account_type = form.cleaned_data["Account_type"]
            Account_type = Account_type.lower()
            if Account_type == "owner":
                registerOwner(form,request)
                if registerAdvertiser(form,request)==1:
                    form = RegisterUserForm()
                    return render(request,"accounts/registrationFailed.html",{'form':form})
            if Account_type == "advertiser":
                if registerAdvertiser(form,request)==1:
                    return render(request,"accounts/registrationFailed.html",{'form':form})
            if Account_type=="administrator":
                if registerAdministrator(form,request)==1:
                    return render(request,"accounts/registrationFailed.html",{'form':form})
        # the if statements for advertiser is not done yet
    else:
        form = RegisterUserForm()
    return render(request, "accounts/registrationtest.html", {'form': form})


def adminTable(request):
    users = Account.objects.all().order_by('name')
    billboards = Billboard.objects.all().order_by('price')
    rents = Rent.objects.all()
    return render(request, "accounts/adminTable.html", {'users': users, 'billboards': billboards, 'rents': rents})


def ownerTable(request):
    users = Account.objects.all().order_by('name')
    billboards = Billboard.objects.all-().order_by('price')
    rents = Rent.objects.all()
    return render(request, "accounts/adminTable.html", {'users': users, 'billboards': billboards, 'rents': rents})


def admin(request):
    users = Account.objects.all().order_by('name')
    account = Account.objects.get(Account_type='administrator')
    billboards = Billboard.objects.all().order_by('price')
    rents = Rent.objects.all()
    requests = Request.objects.filter(to=account)
    return render(request, "accounts/admin.html",
                  {'users': users, 'billboards': billboards, 'rents': rents, 'requests': requests})


def simpleowner(request):
    user= request.user
    account= Account.objects.get(account=user)
    owner = Owner.objects.get(account=account)

    billboards = Billboard.objects.filter(owner=owner)

    requests = Request.objects.filter(to=account)

    message = Message.objects.filter(to=account)
    form = AddBillboardForm()
    return render(request, "accounts/simpleowner.html",
                  {'owner': owner, 'billboards': billboards, 'requests': requests, 'form': form})


def addBillboards(request):
    form = AddBillboardForm(request.POST, request.FILES)
    print("#######################about to enter the if")
    if form.is_valid():
        # photo = form.cleaned_data["photo"]
        print("############################# form is valid")
        owner_id = request.POST['owner_id']
        print("################# owner is: " + str(owner_id))
        name = form.cleaned_data["name"]
        location = form.cleaned_data["location"]
        # replaced this code with the bottom one owner = form.cleaned_data["owner"]
        owner = Owner.objects.get(account=Account.objects.get(id=int(owner_id)))
        price = form.cleaned_data["price"]
        rating = 1
        rawrate = Decimal(1)
        rate_no = 1
        length = form.cleaned_data["length"]
        width = form.cleaned_data["width"]
        image = form.cleaned_data.get("photo")
        #print(type(image))
        newBillboard = Billboard(primary_photo=image, name=name, location=location, owner=owner, price=price,
                                 rating=rating, rate_no=rate_no, rawrate= rawrate,length=length,
                                 width=width, status="requested")
        newBillboard.save()
        typee = "post"
        sender = Account.objects.get(id=owner.account.id)
        to = Account.objects.get(Account_type="administrator")
        billboard = newBillboard
        status = "requested"
        requestt = Request(type=typee, sender=sender, to=to, billboard=billboard, status=status)
        requestt.save()
    return HttpResponseRedirect('/accounts/simpleowner/')


def simpleadvertiser(request):

    return render(request, "accounts/simpleadvertiser.html")

def simpleadmin(request):
    billboards = Billboard.objects.filter(status='requested')
    return render(request, "accounts/simpleadmin.html",{'billboards':billboards})
def acceptBillboardPost(request):
    billboard_id=request.POST['id']
    billboard=Billboard.objects.get(id=billboard_id)
    billboard.status='accepted'
    billboard.save()
    return HttpResponseRedirect('/accounts/simpleadmin/')


def owner(request, account_id):
    # the owner variable is the list of owners that have the account id of account_id
    owner = Owner.objects.get(account=(Account.objects.get(id=account_id)))
    # the account variable below represents the account of the owner
    account = Account.objects.get(id=account_id)
    # the billboards list below is a list that contains all the billboards attributed to the owner(variable) that holds that account_id
    billboards = Billboard.objects.filter(owner=owner)
    # the request list below has all the requests sent to the owner
    requests = Request.objects.filter(to=account)
    # the message list below has all the requests sent to the owner
    message = Message.objects.filter(to=account)

    return render(request, "accounts/owner.html", {'owner': owner, 'billboards': billboards, 'requests': requests})


def advertiser(request, account_id):
    if request.method == 'POST':
        print("#############################################################: 1")
        if 'addAdvertisement' in request.POST:
            form = AddAdvertisementForm(request.POST, prefix='addAdvertisement')
            add_advertisement(form, account_id)
        if 'RentRequest' in request.POST:
            form = RentRequestForm(request.POST, prefix='rentREquest')
            request_rent(form, account_id)
    # the account variable below represents the account of the advertiser
    account = Account.objects.get(id=account_id)

    # the advertiser variable is the list of owners that have the account id of account_id
    advertiser = Advertiser.objects.get(account=(Account.objects.get(id=account_id)))

    # the request list below has all the requests sent by the advertiser
    requests = Request.objects.filter(sender=account)

    # the message list below has all the requests sent to the advertiser
    messages = Message.objects.filter(to=account)

    # the advertisements list below has all the advertisements of the advertiser

    advertisements = Advertisement.objects.filter(Advertiser=advertiser)
    addAdvertisementForm = AddAdvertisementForm(prefix='addAdvertisement')
    rentRequestForm = RentRequestForm(prefix='rentRequest')

    # render an advertiser page with the specific advertiser
    return render(request, "accounts/advertiser.html",
                  {'advertiser': advertiser, 'requests': requests, 'messages': messages,
                   'addAdvertisementForm': addAdvertisementForm, 'rentRequestForm': rentRequestForm})


def add(request):
    if request.method == 'POST':
        form = AddBillboardForm(request.POST)
        if form.is_valid():
            add_billboard_request(form)
    else:
        form = AddBillboardForm()
    return render(request, "accounts/addBillboard.html", {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # log the user in,
            user = form.get_user()
            login(request, user)
            return redirect('billboards:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def login_page(request):
    return render(request, 'accounts/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        try:
            accountt = Account.objects.get(account=request.user)
            advertiser = Advertiser.objects.get(account=accountt)
            print("##########################################advertiser is  set")
        except:
            advertiser = None
            print("##########################################advertiser is not set")
        try:
            accountt = Account.objects.get(account=request.user)
            owner = Owner.objects.get(account=accountt)
        except:
            owner = None
        try:
            accountt = Account.objects.get(account=request.user)
            admin = Administrator.objects.get(account=accountt)
        except:
            admin = None
        if advertiser is not None:
            sentRequests = Request.objects.filter(sender=advertiser.account)

            return render(request, 'accounts/simpleadvertiser.html', {'advertiser': advertiser, 'sentRequests': sentRequests})
        elif owner is not None:

            billboards = Billboard.objects.filter(owner=owner)

            requests = Request.objects.filter(to=accountt)

            message = Message.objects.filter(to=accountt)
            form = AddBillboardForm()
            print("##########################################owner logged in")

            return render(request, 'accounts/simpleowner.html',
                          {'owner': owner, 'billboards': billboards, 'requests': requests, 'form': form})
        elif admin is not None:
            auth.login(request, request.user)

            billboards = Billboard.objects.filter(status='requested')

            requests = Request.objects.filter(to=accountt)

            message = Message.objects.filter(to=accountt)
            print("##########################################admin logged in")

            return render(request, 'accounts/simpleadmin.html',
                          {'admin': admin, 'billboards': billboards})
        else:
            return render(request,"accounts/login_failed.html")

    else:
        print("#########################in the else")
        username = request.POST['username']
        print("#########################inputed username is: " + username)
        password = request.POST['password']
        print("#########################inputed password is: " +
              password)
        user = authenticate(request, username=username, password=password)
        print(type(user))
        try:
            accountt = Account.objects.get(account=user)
            advertiser = Advertiser.objects.get(account=accountt)
            print("##########################################advertiser is  set")
        except:
            advertiser = None
            print("##########################################advertiser is not set")
        try:
            accountt = Account.objects.get(account=user)
            owner = Owner.objects.get(account=accountt)
        except:
            owner = None
        try:
            accountt = Account.objects.get(account=user)
            admin = Administrator.objects.get(account=accountt)
        except:
            admin = None

        if advertiser is not None:
            auth.login(request, user)
            sentRequests = Request.objects.filter(sender=advertiser.account)
            form = rateForm()
            print("##########################################advertiser logged in")
            return render(request, 'accounts/simpleadvertiser.html', {'advertiser': advertiser, 'sentRequests': sentRequests,'form':form})
        elif owner is not None:
            auth.login(request, user)

            billboards = Billboard.objects.filter(owner=owner)

            requests = Request.objects.filter(to=accountt)

            message = Message.objects.filter(to=accountt)
            form = AddBillboardForm()
            print("##########################################owner logged in")

            return render(request, 'accounts/simpleowner.html',
                          {'owner': owner, 'billboards': billboards, 'requests': requests, 'form': form})
        elif admin is not None:
            auth.login(request, user)

            billboards = Billboard.objects.all()

            requests = Request.objects.filter(to=accountt)

            users = Account.objects.all()

            message = Message.objects.filter(to=accountt)
            print("##########################################admin logged in")

            return render(request, 'accounts/simpleadmin.html',
                          {'admin': admin, 'billboards': billboards,'users':users})

        else:
            print("##################################################advertiser is not found")
            return render(request, 'accounts/login_failed.html')


'''def owner_auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/simpleowner.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            accountt = Account.objects.get(account=user)
            advertiser = Advertiser.objects.get(account=accountt)
            print("##########################################advertiser is set")
        except:
            advertiser=None
            print("##########################################advertiser is not set")
        if advertiser is not None:
            auth.login(request, user)
            return render(request, 'accounts/simpleowner.html')
        else:
            print("##################################################advertiser is found")
            return render(request, 'accounts/simpleowner.html')
'''


def logout_view(request):
    auth.logout(request)
    return redirect('accounts:login')


def signin_view(request):
    # this if statement is carried out if the form filled already
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # debug purpose code to see the inputs    print(username+" "+password)
            user = Account.objects.filter(name=username, password=password)
            # debug purpose code to see how many objects are fetched...  print(len(user))

            # the below if statement authenticates the user.
            if (len(user) > 0):
                account = user[0]
                # debug purpose code to check if the right user is being sent to the owner.html print("###############################################the user that logged in is: " + username)
                # return render(request,'accounts/owner.html',{'user':user[0]})
                # the 3 if statements below check the type of user
                if account.Account_type == "owner":
                    print("############################ the type is owner")
                    owner = Owner.objects.get(account=account.id)
                    print("############################" + str(owner.account.name))
                    print("############################" + str(owner.account.id))

                    return redirect('accounts:owner', owner.account.id)

                    # return redire(request, 'accounts/owner.html',{'owner': owner})
                if account.Account_type == "administrator":
                    print("############################ the type is administrator")
                    return redirect('accounts:admin')
                    # the below 2 lines of code are used if there are more tha
                    # administrator = Administrator.objects.get(account=account.id)
                    # return redirect('accounts:admin',administrator.account.id)

                if account.Account_type == "advertiser":
                    print("############################ the type is advertiser")
                    advertiser = Advertiser.objects.get(account=account.id)
                    print("############################" + str(advertiser.account.id))
                    return redirect('accounts:advertiser', advertiser.account.id)
            # this else carried out if the user is not authentic
            else:
                return render(request, 'accounts/registrationtest.html')
    # this else statement is carried out if the form is being requested
    else:
        form = LoginForm()
    return render(request, 'accounts/signin.html', {'form': form})


def signout_view(request, account_id):
    account = Owner.objects.get(id=account_id)
    isAuthenticated.remove(account.id)
    return redirect('BillAd:home')


def accounts(request):
    return render(request, 'accounts/accounts.html')


def billboard_list(request):
    return redirect('billboards:list')
    # billboards = Billboard.objects.all().order_by('rating')
    # return render(request, 'accounts/billboard_list.html', {'billboards': billboards})
    return True


def test(response):
    # form = forms()
    # return render(response, 'accounts/test.html', {'form': form})
    return True
    # the billboard detail function below is messed up


def billboard_detail(request, name):
    # billboard = Billboard.objects.get(name=name)
    # return render(request,'accounts/billboard_detail.html', {'billboard': billboard})
    return True


# Create your views here.


##################################################
# the functions below are not called from any url#
##################################################
## requests are managed below##


def add_billboard_request(form):
    # photo = form.cleaned_data["photo"]
    name = form.cleaned_data["name"]
    location = form.cleaned_data["location"]
    # replaced this code with the bottom one owner = form.cleaned_data["owner"]
    owner = Owner.objects.get(account=Account.objects.get(id=5))
    price = form.cleaned_data["price"]
    rating = form.cleaned_data["rating"]
    length = form.cleaned_data["length"]
    width = form.cleaned_data["width"]
    rent = form.cleaned_data["rent"]
    newBillboard = Billboard(name=name, location=location, owner=owner, price=price, rating=rating, length=length,
                             width=width, status="requested")
    newBillboard.save()
    typee = "post"
    sender = Account.objects.get(id=owner.account.id)
    to = Account.objects.get(Account_type="administrator")
    billboard = newBillboard
    status = "requested"
    requestt = Request(type=typee, sender=sender, to=to, billboard=billboard, status=status)
    requestt.save()
    return True


"""
def accept_post_request(the_rent, the_request):

def reject_post_request(the_rent, the_request):

def accept_rent_request(rent):

def reject_rent_request(rent):
"""


def reject_rent_request(rent):
    return True


# end of request management #

def add_advertisement(form, account_id):
    if form.is_valid():
        print("##############################################################: 3")
        slogan = form.cleaned_data["slogan"]
        description = form.cleaned_data["description"]
        advertiser = Advertiser.objects.get(account=(Account.objects.get(id=account_id)))
        newAdvertisement = Advertisement(slogan=slogan, description=description, Advertiser=advertiser)
        newAdvertisement.save()
        return True


# the bottom function is flashed(hehe) and badly needs to be tested
def request_rent(form, account_id, billboard_id, advertisement_id):
    if form.is_valid():
        print("################################################# inside the rent request function")
        typee = "rent"
        advertiser = Advertiser.objects.get(account=Account.objects.get(id=account_id))
        sender = Account.objects.get(id=advertiser.account.id)
        billboard = form.cleaned_data("billboard")
        to = billboard.owner
        status = "requested"
        startDate = form.cleaned_data("startDate")
        endDate = form.cleaned_data("endDate")
        advertisement = form.cleaned_data("advertisement")
        requestt = Request(type=typee, sender=sender, to=to, billboard=billboard, status=status)
    return True

def registerOwner(form,request):
    if form.is_valid():
        #profile_picture = form.cleaned_data["profile_picture"]

        name = form.cleaned_data["name"]
        try:
            user = User.objects.get(username=name)
            print()
            if getattr(user,'username') == name:
                print("in the if statement")
                return (1)
        except:
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            newUser = User.objects.create_user(username=name, password=password, email=email)
            newUser.save()
            newAccount = Account(account=newUser, name=name, phone_number=phone_number, email=email, password=password,
                                 Account_type="owner", rating=1)
            newAccount.save()
            newOwner = Owner(account=newAccount, preferred_content="test")
            newOwner.save()
            owner = Owner.objects.get(account=newOwner.account.id)
            print("############################" + str(owner.account.id))
            return redirect('accounts:owner', owner.account.id)


def registerAdvertiser(form,request):
    if form.is_valid():
        name = form.cleaned_data["name"]
        print("#####################################################in the register advertiser function")
        try:
            user = User.objects.get(username=name)
            print()
            if getattr(user,'username') == name:
                print("in the if statement")
                return (1)
        except:
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            print("##################################################### back in the register advertiser function")
            newUser = User.objects.create_user(username=name, password=password, email=email)
            newUser.save()
            newAccount = Account(account=newUser, name=name, phone_number=phone_number, email=email, password=password,
                                 Account_type="owner", rating=1)
            newAccount.save()
            newAdvertiser = Advertiser(account=newAccount, rented_billboards="none")
            newAdvertiser.save()
            advertiser = Advertiser.objects.get(account=newAdvertiser.account.id)

            return redirect('accounts:advertiser', advertiser.account.id)


def registerAdministrator(form, request):
    if form.is_valid():
        name = form.cleaned_data["name"]
        print("#####################################################in the register advertiser function")
        try:
            user = User.objects.get(username=name)
            print()
            if getattr(user, 'username') == name:
                print("in the if statement")
                return (1)
        except:
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            print("##################################################### back in the register advertiser function")
            newUser = User.objects.create_user(username=name, password=password, email=email)
            newUser.save()
            newAccount = Account(account=newUser, name=name, phone_number=phone_number, email=email, password=password,
                                 Account_type="administrator", rating=1)
            newAccount.save()
            newAdministrator = Administrator(account=newAccount)
            newAdministrator.save()
            advertiser = Administrator.objects.get(account=newAdministrator.account.id)

            return redirect('accounts:advertiser', advertiser.account.id)


def delete(request):
    billboard_id = request.POST['id']
    billboard = Billboard.objects.get(id=billboard_id)
    billboard.delete()
    return HttpResponseRedirect('/accounts/simpleowner/')


# this wroks it accepts a rent request for a billboard, it changes the status of a request to accepted
def accept_rent_request(request):
    request_id = request.POST['id']
    requestt = Request.objects.get(id=request_id)
    print("###########################################")
    print(type(requestt))
    print(requestt.sender.account)
    requestt.status = 'accepted'
    requestt.save()
    print("##################### inside the accept rent request function")
    print("request id: " +str(request_id))
    return HttpResponseRedirect('/accounts/simpleowner/')


# this wroks it declines a rent request for a billboard, it changes the status of a request to declined
def decline_rent_request(request):
    request_id = request.POST['id']
    requestt = Request.objects.get(id=request_id)
    requestt.status = 'declined'
    requestt.save()
    return HttpResponseRedirect('/accounts/simpleowner/')

def rateBillboard(request):
    advertiser=Advertiser.objects.get(account=Account.objects.get(account=request.user))
    sentRequests = Request.objects.filter(sender=advertiser.account)
    rate = request.POST['id']
    billboard= request.POST['billid']
    print("000000000000000000000000000000000000 " + str(rate))
    print(billboard)
    if rating_system(rate,billboard):
        print("im a freaking genius")
    return HttpResponseRedirect('/accounts/simpleadvertiser/')


def rating_system(user_rating,billboard_id):
    billboard = Billboard.objects.get(id=billboard_id)
    rateRaw = billboard.rawrate
    rate_no = billboard.rate_no
    rating = billboard.rating
    print(type(rateRaw))
    newRating = (rateRaw*Decimal(rate_no))+ Decimal(user_rating) / Decimal(rate_no+1)
    print(type(newRating))
    newRateRaw = newRating
    newRating = math.ceil(newRateRaw)
    newRateNo= billboard.rate_no + 1
    billboard.rawrate = newRateRaw
    billboard.rating = newRating
    billboard.rateNo = newRateNo
    print("1111111111111111111111111111111111111111111")
    print(newRateRaw)
    print(newRating)
    print(newRateNo)
    return True





def profile_server(request):
    user = request.user
    try:
        accountt = Account.objects.get(account=user)
        if accountt.Account_type=='owner':
            owner = Owner.objects.get(account=accountt)
            billboards = Billboard.objects.filter(owner=owner)

            requests = Request.objects.filter(to=accountt)

            message = Message.objects.filter(to=accountt)
            form = AddBillboardForm()
            print("##########################################owner logged in")

            return render(request, 'accounts/simpleowner.html',
                          {'owner': owner, 'billboards': billboards, 'requests': requests, 'form': form})
        if accountt.Account_type == 'advertiser':
            advertiser =Advertiser.objects.get(account=accountt)
            sentRequests = Request.objects.filter(sender=advertiser.account)
            form = rateForm()
            print("##########################################advertiser logged in")
            return render(request, 'accounts/simpleadvertiser.html',
                          {'advertiser': advertiser, 'sentRequests': sentRequests, 'form': form})
        if accountt.Account_type == 'administrator':
            billboards = Billboard.objects.all()

            requests = Request.objects.filter(to=accountt)

            users = Account.objects.all()

            message = Message.objects.filter(to=accountt)
            print("##########################################admin logged in")

            return render(request, 'accounts/simpleadmin.html',
                          {'admin': admin, 'billboards': billboards, 'users': users})
    except:
        logout_view(request)


