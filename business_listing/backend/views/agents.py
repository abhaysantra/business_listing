from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.conf import settings

# Create your views here.
from backend.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from backend.models import *
from backend.decorators import *
from backend.forms import *
import os, sys

@login_required()
def agentList(request):
    agents= MyUser.objects.filter(user_type_id=2)
    return render(request,'agent/agent_list.html',{'agents':agents,'agentlist_active':'active'})

@login_required()
def getVendorList(request, uuid_code):
    print('Agent with uuid_code : ',uuid_code)
    user_id = MyUser.objects.get(uuid_code=uuid_code)
    vendorlistUderThisAgent = VendorList.objects.filter(agent_id=user_id).values_list('vendor_id',flat=True) 
    print('vendorlistUderThisAgent: ',vendorlistUderThisAgent)

    vendorList= MyUser.objects.filter(id__in = vendorlistUderThisAgent)
    return render(request,'agent/vendor_list.html',{'vendorList':vendorList,'agentlist_active':'active'})

@login_required()
def addVendor(request):
    print('When adding vendorAgent with id : ',request.user.id)
    
    # user = MyUser.objects.get(id=pk)
    # myProfile = MyUserProfile.objects.get(user=user)
    if request.method == 'POST':
        userform = UpdateUserForm(request.POST,request.FILES)#, instance=user)
        userProfileForm = UpdateUserProfileForm(request.POST,request.FILES) #,instance=myProfile)
        if userform.is_valid() and userProfileForm.is_valid():
            user = userform.save(commit=False)
            user.user_type_id = 3
            user.save()
            userProfile = userProfileForm.save(commit=False)
            userProfile.user_id = user.id
            userProfile.modified_date = datetime.now()
            userProfile.save()

            # make a vendorlist based on agent
            obj = VendorList(vendor_id=user.id, agent_id = request.user.id)
            obj.save()
            return redirect('admin_index')
        else:
        	print('error in vendor add form')
        	for i in userform.errors:
        		print(i)

    userform = UpdateUserForm()
    profileform = UpdateUserProfileForm()
    context = {'form':userform,'profileform':profileform,'addvendor_active':'active'}
    return render(request, 'edit_profile_using_form.html', context)

@login_required()
def individual_vendor_list(request):
	# ------------ dont need calculation as we have added a field for is_individual_vendor ----#
	# # now find all vendors whose user_type_id = 3
	# allVendors = MyUser.objects.filter(user_type_id=3).values_list('id', flat=True).order_by('id')
	# allVendors = [i for i in allVendors]
	# print('allVendors :',allVendors)
	# #now find all vendors who are under any agents
	# allVendorsUnderAgents = VendorList.objects.all().values_list('vendor_id', flat=True).order_by('id')
	# allVendorsUnderAgents = [i for i in allVendorsUnderAgents]
	# print('allVendorsUnderAgents :',allVendorsUnderAgents)
	# individual_vendors = [x for x in allVendors if x not in allVendorsUnderAgents]
	# print('individual_vendors :',individual_vendors)

	vendorList= MyUser.objects.filter(is_individual_vendor = 1, user_type_id=3)
	return render(request,'agent/vendor_list.html',{'vendorList':vendorList,'vendorlist':'active'})

@login_required()
def deleteVendor(request, uuid_code):
    vendor_obj= MyUser.objects.get(uuid_code = uuid_code)
    # remove stored image from system
    # remove_old_image_from_system(vendor_obj.picture)
    vendor_obj.delete()
    return redirect('getvendorlist', uuid_code=request.user.uuid_code)


