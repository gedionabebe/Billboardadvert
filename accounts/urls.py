from django.contrib import admin
from django.urls import include, path
from . import views


app_name = 'accounts'

urlpatterns = [

    path('', views.accounts),
    path('login_page/', views.login_page, name="login_page"),
    path('login_processer',views.auth_view, name="login_processer"),
    path('logout_view',views.logout_view, name="logout_view"),
    path('billboards/', views.billboard_list),
    path('registration/', views.registration, name="registration"),
    path('login/', views.login_page, name="login"),
    path('detail/', views.billboard_detail),
    path('add/', views.add, name="addBillboard"),
    #path('signin/', views.signin_view, name="signin"),
    path('<int:account_id>/', views.advertiser, name="advertiser"),
    path('<int:account_id>/', views.owner, name="owner"),
    path('registrationtest/', views.registrationtest, name="registrationtest"),
    path('admin/', views.admin, name="admin"),
    path('adminTable/', views.adminTable, name="adminTable"),
    path('ownerTable/', views.ownerTable, name="ownerTable"),
    path('simpleowner/', views.simpleowner, name='simpleowner'),
    path('delete/', views.delete,name="delete"),
    path('acceptRentRequest/', views.accept_rent_request, name="acceptRentRequest"),
    path('declineRentRequest/', views.decline_rent_request, name="declineRentRequest"),
    path('addBillboards/', views.addBillboards, name="addBillboards"),
    path('simpleadvertiser/', views.simpleadvertiser, name="simpleadvertiser"),
    path('simpleadmin/', views.simpleadmin, name="simpleadvertiser"),
    path('acceptBillboardPost/', views.acceptBillboardPost, name="acceptBillboardPost"),
    path('rateBillboard/', views.rateBillboard, name="rateBillboard"),
    path('profile_server/', views.profile_server, name="profile_server"),
]

