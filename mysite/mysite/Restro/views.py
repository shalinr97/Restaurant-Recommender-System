from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.core.paginator import Paginator
from yelpapi import YelpAPI
from django.conf import settings
import requests
import random
import json
import pandas as pd
from .recommender import recommender
yelp_api = YelpAPI(settings.YELP_API_KEY)

# Create your views here.
def home(request):
    return render(request, 'home.html')

# def restaurant_listview(request):
#     template_name = 'restaurants/restaurant_listview.html'
#     queryset = Restaurant.objects.all()
#     paginator = Paginator(queryset,10)
#     page = request.GET.get('page')
#     #page_k=5
#     queryset=paginator.get_page(page)
#     context = {
#         "object_list": queryset

#     }
#     return render(request, template_name, context)

def detailed(request, my_id):
  template_name = 'restaurants/restaurant_details.html'
  queryset = Restaurant.objects.get(id=my_id)
  context = {
        "object_list": queryset

    }
  return render(request, template_name,context)

def search(request):

    template_name = 'demo.html'
    search_name = request.GET.get('search')
    location = "NEW YORK"
    template_name = 'demo.html'

    #search_name = request.GET.get('search')
    # location = 'New York'
    # query_set = yelp_to_db(search_name,location)
    # context = {
    #      object_list : search_name
    # }

    return render(request,template_name)

def search_result(request):

  template_name = 'details.html'
  location = request.GET.get('location')
  search_name = request.GET.get('search')
  price = request.GET.get('budget')
  yelp_restaurant_object= []
  # params = {
  #           'limit': 50,
  #           'location': 'New York',
  #           'price': price,
  #           'term': search_name,
  #         }
  for offset in range(0,200,20):

    search_results = yelp_api.search_query(term = search_name, location = location, price = price, sort=0,offset= offset)
    yelp_restaurant_object += search_results['businesses']
  #yelp_restaurant_object = search_results['businesses']
  query_set = yelp_restaurant_object
  #query_set = yelp_to_db(search_name,location,params)

  context = {
          "object_list" : query_set
      }


  return render(request,template_name, context)

def test(request):

  template_name = 'test.html'
  return render(request,template_name)

def dummy(request):
  template_name = 'dummy.html'
  lucky = random.randint(0, 43355)
  business_final = recommender(request,lucky) #temporarily removed
  name_list = business_final['business_name'].tolist()

 
  context = {
          "object_list" : name_list,
          "random_user": lucky,
          
    }

  return render(request, template_name,context)








'''
<!-- {% for posts in object_list %}
{{posts.number}}
{{posts.paginator.count}}
{{posts.paginator.num_pages}}
{{posts.paginator.page_range}}

{%if object_list.numer == num %}
  <strong>{{ num }} </strong>
{%else}
  {{ num }}
{%endif}
  {{ num }}



  {%for num in object_list.paginator.page_range %}

  {%end for%}
-->
'''
