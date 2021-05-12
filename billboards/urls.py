from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'billboards'

urlpatterns = [
   
    path('', views.BillboardList, name="BillboardList"),
    path('rentt/', views.rent, name="rent"),
    path('<int:billboard_id>/', views.detail, name="detail"),
    path('rent/<int:billboard_id>/', views.rent, name="rentBillboard"),
    path('search/', views.SearchResultsView, name="search_results"),
    path('ownerpage/<int:billboard_id>/', views.Owner_page, name="ownerpage"),
    path('filter/', views.Filter, name="filter_results"),#copy this

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
