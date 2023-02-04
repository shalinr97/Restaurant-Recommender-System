from django.contrib import admin
from django.urls import path, include
from . import views
#from Restro.views import restaurant_listview


urlpatterns = [
#path('restaurant/', restaurant_listview,name='restaurant'),
path('restaurant/<int:my_id>/', views.detailed, name="detailed"),
path('search/',views.search,name="search"),
path('searchresult/',views.search_result, name="searchresult"),
path('test/',views.test, name="test"),
path('recommend/',views.dummy, name="recommend")
]
