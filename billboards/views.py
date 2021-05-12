from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Billboard
from accounts.models import *
from accounts.models import Owner
from .models import Request,Rent
from .forms import RentRequestForm
from .forms import FilterForm#copy 
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def BillboardList(request):
    billboards = Billboard.objects.filter(status='accepted').order_by('rating')
    filter_form = FilterForm()
    if request.user.is_authenticated:
        userr=request.user
        return render(request, 'billboards/billboard_list.html', {'billboards': billboards, 'userr':userr})
    return render(request, 'billboards/billboard_list.html', {'billboards': billboards, 'filter_form':filter_form})


def rent(request, billboard_id):
    billboard_id = Billboard.objects.all()
    return render(request, ',,,')


def detail(request, billboard_id):
    ''' so this function might be a little hard to explain but what it basically
    does is it filters all the unrented months of the specific billboard and it
    sends those months to the details page of that specific billboards it does
    this so that the already rented months of the billboard wouldnt be presented
    as options in the details page '''
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    singleBillboard = Billboard.objects.get(id=billboard_id)
    accepted_requests = Request.objects.filter(status='accepted')
    rented_months=[]
    month_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                  'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 7, 'october': 10,
                  'november': 11, 'december': 12}
    field_name = 'startDate'
    accepted_rents_list = []
    print("accepted requests:" + str(accepted_requests))
    for requestt in accepted_requests:
        accepted_rents = Rent.objects.filter(request_id=requestt)
        accepted_rents_list.append(accepted_rents)
        print(accepted_rents_list)
    print("test" + str(accepted_rents_list))
    start_date_months=[]
    keys = list(month_dict.keys())
    values = list(month_dict.values())
    print(accepted_rents_list)
    for rent in accepted_rents_list:
        print(rent)
        #this bottom one tries to get a queryset with a rent in it and if the query set is empty it goes to the except block
        print(len(rent))
        try:
            for i in range(0, len(rent)):
                if rent[i].billboard == singleBillboard:
                    print(rent[i].billboard)
                    start_date = getattr(rent[i], field_name)
                    print(start_date)
                    print("start_date.month =  "+str(start_date.month))
                    for month, idd in month_dict.items():
                        print(month+" : "+ str(idd))
                        if idd == start_date.month:
                            print("###################wazaa")
                            print("###############"+str(idd))
                            print("###############" + str(month))
                            months.remove(month)

        except:
            continue
    print(months)

    if request.user.is_authenticated:
        '''rating = getattr(singleBillboard, 'rating')
        print("0000000000000000000000000000000000000000000000000000000000000000000000")
        print(rating)'''
        form = RentRequestForm()
        rating = singleBillboard.rating
        rating_checked_list = []
        rating_empty_list=[]
        print("0000000000000000000000000000000000000000000000000000000000000000000000")
        print(rating)
        userr = request.user
        for i in range(rating):
            rating_checked_list.append(i)
        rating_left = 5-rating
        print(rating_left)
        for i in range(rating_left):
            rating_empty_list.append(i)
        print(len(rating_empty_list))
        return render(request, 'billboards/billboardDetail.html', {'singleBillboard': singleBillboard,
                        'form': form, 'months': months, 'rating': rating, 'rating_checked_list': rating_checked_list,
                        'rating_empty_list':rating_empty_list, 'userr':userr})
    else:
        return render(request, 'billboards/billboardDetail.html', {'singleBillboard': singleBillboard})


@login_required
def rent(request):
    months = request.POST.getlist('months')
    # this dict maps each month from string to number eg. we get a 'january' month and we map it into '01'
    month_dict = {'january': '01',  'february': '02', 'march': '03', 'april': '04',
                  'may': '05', 'june': '06', 'july': '07', 'august': '08', 'september': '09', 'october': '10',
                  'november': '11', 'december': '12'}
    # this dict for the number of days in a month
    days_in_months={'january': '31',  'february': '28', 'march': '31', 'april': '30',
                  'may': '31', 'june': '30', 'july': '31', 'august': '31', 'september': '30', 'october': '31',
                  'november': '30', 'december': '31'}
    user = request.user
    print("########################## rent request sender: " + user.username)
    accountt = Account.objects.get(account=user)
    advertiser = Advertiser.objects.get(account=accountt)
    billboard_id = request.POST['billboard_id']
    print("Billboard id: " + str(billboard_id))
    billboard = Billboard.objects.get(id=int(billboard_id))
    owner = billboard.owner
    receiver = owner.account
    newRequest = Request(type="rent", sender=accountt, to=receiver, billboard=billboard, status="requested")
    newRequest.save()
    for month in months:
        month_id = month_dict[month]
        start_date = '01/'+month_id+'/20'
        start_date = datetime.strptime(start_date, '%d/%m/%y').date()
        print("start date: " + str(start_date))
        end_month_days = days_in_months[month]
        end_date = end_month_days+'/'+month_id+'/20'
        print(end_date)
        end_date = datetime.strptime(end_date, '%d/%m/%y').now().date()
        print(type(end_date))
        newRent = Rent(startDate=start_date, endDate=end_date, advertiser=advertiser,
                       billboard=billboard, request_id=newRequest)
        newRent.save()

    print("months= " + str(months))
    return HttpResponseRedirect('/billboards/')
searchresults=[]
def searchResultCheck():
    return searchresults 
def SearchResultsView(request):
    filter_form = FilterForm()
    if request.GET:
        query = request.GET['q']
        print(query)
        billboards = Billboard.objects.filter(
            #Q(owner__icontains=query) |
            Q(location__icontains=query) |
            Q(name__icontains=query)).order_by('rating').reverse()
        for billboard in billboards:
            searchresults.append(billboard)
        return render(request, 'billboards/search_results.html', {'billboards':billboards, 'filter_form':filter_form})
def Owner_page(request, billboard_id):
    ownerid = Billboard.objects.get(id=billboard_id).owner
    billboards= Billboard.objects.all()
    ownerbills=[]
    ownerdetails=[]
    ownerdetails.append(ownerid)
    for billboard in billboards:
        if billboard.owner == ownerid:
            ownerbills.append(billboard)
        

    return render(request, 'billboards/Owner_page.html', {'ownerbills': ownerbills, 'ownerdetails':ownerdetails})
#copy this
def Filter(request):    
    form = FilterForm(request.POST)
    filter_form = FilterForm()
    if form.is_valid():
        price_range= form.cleaned_data["price_range"]
        size_range= form.cleaned_data["size_range"]
        if price_range == 'budget' or size_range == 'small':
            billboards = Billboard.objects.filter(
                Q(price__lte=10000, price__gte=0) | 
                Q(width__lte=10, width__gte=1)
                ).order_by('rating').reverse()
        elif price_range == 'budget' or size_range == 'medium':
            billboards = Billboard.objects.filter(
                Q(price__lte=10000, price__gte=0) | 
                Q(width__lte=15, width__gte=10)
                ).order_by('rating').reverse()
        elif price_range == 'budget' or size_range == 'large':
            billboards = Billboard.objects.filter(
                Q(price__lte=10000, price__gte=0) | 
                Q(width__lte=20, width__gte=15)
                ).order_by('rating').reverse()
        elif price_range == 'budget' or size_range == 'extralarge':
            billboards = Billboard.objects.filter(
                Q(price__lte=10000, price__gte=0) | 
                Q(width__lte=25, width__gte=20)
                ).order_by('rating').reverse()
        elif price_range == 'midrange' or size_range == 'small':
            billboards = Billboard.objects.filter(
                Q(price__lte=15000, price__gte=10000) |
                Q(width__lte=10, width__gte=1)
                ).order_by('rating').reverse()
        elif price_range == 'midrange' or size_range == 'medium':
            billboards = Billboard.objects.filter(
                Q(price__lte=15000, price__gte=10000) |
                Q(width__lte=15, width__gte=10)
                ).order_by('rating').reverse()
        elif price_range == 'midrange' or size_range == 'large':
            billboards = Billboard.objects.filter(
                Q(price__lte=15000, price__gte=10000) |
                Q(width__lte=20, width__gte=15)
                ).order_by('rating').reverse()
        elif price_range == 'midrange' or size_range == 'extralarge':
            billboards = Billboard.objects.filter(
                Q(price__lte=15000, price__gte=10000) |
                Q(width__lte=25, width__gte=20)
                ).order_by('rating').reverse()
        elif price_range == 'uppermidrange' or size_range == 'small':
            billboards = Billboard.objects.filter(
                Q(price__lte=20000, price__gte=15000) |
                Q(width__lte=10, width__gte=1)
                ).order_by('rating').reverse()
        elif price_range == 'uppermidrange' or size_range == 'small':
            billboards = Billboard.objects.filter(
                Q(price__lte=20000, price__gte=15000) |
                Q(width__lte=10, width__gte=1)
                ).order_by('rating').reverse()
        elif price_range == 'uppermidrange' or size_range == 'medium':
            billboards = Billboard.objects.filter(
                Q(price__lte=20000, price__gte=15000) |
                Q(width__lte=15, width__gte=10)
                ).order_by('rating').reverse()
        elif price_range == 'uppermidrange' or size_range == 'large':
            billboards = Billboard.objects.filter(
                Q(price__lte=20000, price__gte=15000) |
                Q(width__lte=20, width__gte=15)
                ).order_by('rating').reverse()
        elif price_range == 'uppermidrange' or size_range == 'extralarge':
            billboards = Billboard.objects.filter(
                Q(price__lte=20000, price__gte=15000) |
                Q(width__lte=25, width__gte=20)
                ).order_by('rating').reverse()
        elif price_range == 'highend' or size_range == 'small':
            billboards = Billboard.objects.filter(
                Q(price__lte=25000, price__gte=20000) |
                Q(width__lte=10, width__gte=1)
                ).order_by('rating').reverse()
        elif price_range == 'highend' or size_range == 'medium':
            billboards = Billboard.objects.filter(
                Q(price__lte=25000, price__gte=20000) |
                Q(width__lte=15, width__gte=10)
                ).order_by('rating').reverse()
        elif price_range == 'highend' or size_range == 'large':
            billboards = Billboard.objects.filter(
                Q(price__lte=25000, price__gte=20000) |
                Q(width__lte=20, width__gte=15)
                ).order_by('rating').reverse()
        elif price_range == 'highend' or size_range == 'extralarge':
            billboards = Billboard.objects.filter(
                Q(price__lte=25000, price__gte=20000) |
                Q(width__lte=25, width__gte=20)
                ).order_by('rating').reverse()

        
        return render(request, 'billboards/filter_results.html', {'billboards':billboards, 'filter_form':filter_form})
#till here

        