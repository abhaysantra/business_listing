from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from backend.models import *
from backend.decorators import *

#set global; variables to access at some other files
selected_parlour_id = None

def get_state_list(request):
    country_id = request.POST['country_id']
    state_obj_list = States.objects.filter(country_id=country_id)
    state_dict = {}
    for state in state_obj_list:
        state_dict[str(state.state_id)] = state.name
    return JsonResponse(state_dict)

def get_city_list(request):
    state_id = request.POST['state_id']
    cities_obj_list = Cities.objects.filter(state_id=state_id)
    city_dict = {}
    for city in cities_obj_list:
        city_dict[str(city.city_id)] = city.name
    return JsonResponse(city_dict)
