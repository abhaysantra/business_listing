from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse

# Create your views here.
from backend.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from backend.models import *
from backend.decorators import *
from backend.forms import *
from .import common
import os, sys

@login_required()
def list_parlour(request):
    parlour_list= Parlour.objects.filter(agent_id = request.user.id).order_by('-id')
    return render(request,'parlour/list_parlour.html',{'parlour_list':parlour_list,'parlour_service':'active'})

@login_required()
def add_parlour(request):
    try:
        if request.method == 'POST':
            parlourform = ParlourCreationForm(request.POST,request.FILES)
            if parlourform.is_valid():
                print(request.POST.get('phone_number',None))
                parlour = parlourform.save(commit=False)
                parlour.agent = request.user
                parlour.save()

                 # checking with ModelManager => ParlourManager
                return_status = Parlour.parman.check_phonenumber(parlour.phone_number)
                print('return_status :',return_status)
                # userProfile.modified_date = datetime.now()
                return redirect('list-parlour')
            else:
                print('error in vendor add form:...')
                print(request.POST)
                for i in parlourform.errors:
                    print(i)

        all_countries = Countries.objects.all()

        parlourform = ParlourCreationForm()
        print('logged iin id :',request.user.id)
        vendor_list = VendorList.objects.filter(agent_id=request.user.id).values_list('vendor_id', flat=True)
        vendor_list_with_details = MyUser.objects.filter(id__in=vendor_list)
        print('vendor_list_with_details : ',vendor_list_with_details)
        return render(request,'parlour/add_parlour.html',{'parlourform':parlourform,'parlour_service':'active', 'vendor_list':vendor_list_with_details,'all_countries':all_countries})
    except Exception as e:
        print('exception : ',e)
        return render(request,'no-result-found.html',{})

@login_required()
def edit_parlour(request, uuid_code):
	try:
	    parlour_obj= Parlour.objects.get(uuid_code = uuid_code)
	    previous_picture = parlour_obj.picture
	    print('previous_picture :',previous_picture)
	    if request.method == 'POST':
	        parlourform = ParlourCreationForm(request.POST,request.FILES, instance = parlour_obj)
	        if parlourform.is_valid():
	            parlour = parlourform.save(commit=False)
	            parlour.modified_date = datetime.now()
	            # remove old image from system when image updated
	            if request.FILES:
	                remove_old_image_from_system(previous_picture)

	            parlour.save()
	            return redirect('list-parlour')
	        else:
	            print('error in vendor add form:...')
	            for i in parlourform.errors:
	                print('Error in : ',i)

	    all_countries = Countries.objects.all()
	    all_states = States.objects.filter(country_id = parlour_obj.country)
	    all_cities = Cities.objects.filter(state_id = parlour_obj.state)

	    parlourform = ParlourCreationForm(instance = parlour_obj)
	    vendor_list = VendorList.objects.filter(agent_id=request.user.id).values_list('vendor_id', flat=True)
	    vendor_list_with_details = MyUser.objects.filter(id__in=vendor_list)#.values_list('id',flat=True)
	    # print('vendor_list_with_details : ',vendor_list_with_details[0].id)
	    # print('parlourform.vendor :',parlour_obj.vendor_id)
	    context = {'parlourform':parlourform,
	                'parlour_service':'active',
	                'vendor_list':vendor_list_with_details,
	                'all_countries':all_countries,
	                'all_states':all_states,
	                'all_cities':all_cities,
	                'parlour_obj':parlour_obj,
	                }
	    return render(request,'parlour/edit_parlour.html',context)
	except Exception as e:
		print('exception : ',e)
		return render(request,'no-result-found.html',{})

def remove_old_image_from_system(previous_picture):
    list_image_url = settings.BASE_DIR+'/media/'+previous_picture.name
    print('list_image_url: ',list_image_url)
    #list_image_url = list_image_url.replace('/','\\')
    try:
        os.remove(list_image_url)
    except Exception as e:
        print('unable to delete image : ',e)

@login_required()
def change_status(request):
    status = request.POST['status']
    id_list = request.POST.getlist('id[]')

    for each_id in id_list:
        each_obj = Parlour.objects.get(id=each_id)
        each_obj.status = status
        each_obj.save()

    return JsonResponse({'result': '1'})

@login_required()
def delete_parlour(request, uuid_code):
    parlour_obj= Parlour.objects.get(uuid_code = uuid_code)
    # remove stored image from system
    remove_old_image_from_system(parlour_obj.picture)
    parlour_obj.delete()
    return redirect('list-parlour')

################# For PARLOUR SERVICES ##################
@login_required()
def list_parlour_service(request,uuid_code):
    parlour_obj = Parlour.objects.get(uuid_code=uuid_code)
    parlour_id = parlour_obj.id
    parlour_service_list= ParlourService.objects.filter(parlour_id = parlour_id)
    common.selected_parlour_id = parlour_id
    common.selected_parlour_uuid_code = uuid_code
    print('Parlour id %s and uuid= %s :' %(common.selected_parlour_id,common.selected_parlour_uuid_code))

    return render(request,'parlour/services/list_parlour_service.html',{'parlour_service_list':parlour_service_list,'parlour_service':'active'})


@login_required()
def add_parlour_service(request):
    try:
        if request.method == 'POST':
            parlourserviceform = ParlourServiceCreationForm(request.POST,request.FILES)
            if parlourserviceform.is_valid():
                # print(request.POST)
                parlourservice = parlourserviceform.save(commit=False)
                print('common.selected_parlour_id affter service creation :',common.selected_parlour_id)
                parlourservice.parlour_id = common.selected_parlour_id
                parlourservice.save()
                # userProfile.modified_date = datetime.now()
                return redirect('list-parlour-service', uuid_code=common.selected_parlour_uuid_code)
            else:
                print('error in vendor add form:...')
                print(request.POST)
                for i in parlourserviceform.errors:
                    print(i)

        parlourserviceform = ParlourServiceCreationForm()
        return render(request,'parlour/services/add_parlour_service.html',{'parlourform':parlourserviceform,'parlour_service':'active','parlour_uuid_code':common.selected_parlour_uuid_code})
    except Exception as e:
        print('exception : ',e)
        return render(request,'no-result-found.html',{})

@login_required()
def edit_parlour_service(request, uuid_code):
    try:
        parlour_obj= ParlourService.objects.get(uuid_code = uuid_code)
        # previous_picture = parlour_obj.picture
        # print('previous_picture :',previous_picture)
        if request.method == 'POST':
            parlourform = ParlourServiceCreationForm(request.POST,request.FILES, instance = parlour_obj)
            if parlourform.is_valid():
                parlour = parlourform.save(commit=False)
                parlour.modified_date = datetime.now()
                # remove old image from system when image updated
                # if request.FILES:
                #     remove_old_image_from_system(previous_picture)

                parlour.save()
                return redirect('list-parlour-service',uuid_code=parlour_obj.parlour.uuid_code)
            else:
                print('error in vendor add form:...')
                for i in parlourform.errors:
                    print('Error in : ',i)

        parlourform = ParlourServiceCreationForm(instance = parlour_obj)
        context = {'parlourform':parlourform,
                    'parlour_service':'active',
                    'parlour_obj':parlour_obj,
                    # 'parlour_uuid_code':common.selected_parlour_uuid_code,
                    }
        return render(request,'parlour/services/edit_parlour_service.html',context)
    except Exception as e:
        print('exception : ',e)
        return render(request,'no-result-found.html',{})

@login_required()
def change_status_parlour_service(request):
    status = request.POST['status']
    id_list = request.POST.getlist('id[]')

    for each_id in id_list:
        each_obj = ParlourService.objects.get(id=each_id)
        each_obj.status = status
        each_obj.save()

    return JsonResponse({'result': '1'})

@login_required()
def delete_parlour_service(request, uuid_code):
    parlour_obj= ParlourService.objects.get(uuid_code = uuid_code)
    # remove stored image from system
    # remove_old_image_from_system(parlour_obj.picture)
    parlour_obj.delete()
    return redirect('list-parlour-service',uuid_code=parlour_obj.parlour.uuid_code)