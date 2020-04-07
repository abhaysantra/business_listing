from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from .models import *

def login(request):
    return render(request, 'login.html')

def login_action(request):
    login_email = request.POST["login_email"]
    login_password = request.POST["login_password"] 
    # print(login_email,login_password)
    check_login = User.objects.filter(login_email=login_email,login_password=login_password)
    if check_login:
        if check_login[0].user_type_id==1:
            request.session['admin_session_id'] = check_login[0].id
            request.session['admin_session_name'] = check_login[0].full_name
            return redirect(index)
        else:
            messages.error(request,'username or password not correct')
            return redirect(login)
    else:
        messages.error(request,'username or password not correct')
        return redirect(login)  

def logout(request):
    del request.session['admin_session_id']
    del request.session['admin_session_name']
    messages.info(request,'Successfully Logout!')
    
    return redirect(login)

def index(request):
    if 'admin_session_id' not in request.session:
        return redirect(login)
    else:
        all_product = User.objects.all()
        all_category = User.objects.all()
        all_enquiry = User.objects.all()
        all_users = User.objects.filter(user_type_id = 2).order_by('-id')
        all_brands = User.objects.all()
        all_orders = User.objects.all()
        context = {
            'all_product':all_product,
            'all_category':all_category,
            'all_enquiry':all_enquiry,
            'all_users':all_users,
            'all_brands':all_brands,
            'all_orders':all_orders
        }
        return render(request, 'dashboard_view.html', context)

def admin_profile(request):
    if 'admin_session_id' not in request.session:
        return redirect(login)

    admin_session_id = request.session['admin_session_id']
    profile_data = adminUser.objects.get_or_create(id=admin_session_id)
   
    return render(request, 'admin_profile_edit.html', {'profile_data':profile_data})

def admin_profile_edit(request):
    full_name = request.POST["full_name"]
    email = request.POST["email"]
    userid = request.POST["userid"]

    profile_data = User.objects.get_or_create(id=userid)[0]
    profile_data.full_name = full_name
    profile_data.login_email = email
    profile_data.save(update_fields=['full_name', 'login_email'])

    messages.info(request,'Profile Successfully Updated!')

    return redirect(admin_profile)

def admin_password_view(request):
    if 'admin_session_id' not in request.session:
        return redirect(login)

    admin_session_id = request.session['admin_session_id']
    profile_data = User.objects.get_or_create(id=admin_session_id)
   
    return render(request, 'admin_password_change.html', {'profile_data':profile_data})

def admin_password_update(request):
    if 'admin_session_id' not in request.session:
        return redirect(login)

    con_pass = request.POST["con_pass"]
    hidden_user_id = request.POST["hidden_user_id"]
    
    adminObj = User.objects.get_or_create(id=hidden_user_id)[0]
    adminObj.login_password = con_pass
    adminObj.save(update_fields=['login_password'])

    messages.info(request,'Password Successfully Updated!')

    return redirect(admin_password_view)

def admin_email_view(request):
    if 'admin_session_id' not in request.session:
        return redirect(login)

    admin_session_id = request.session['admin_session_id']
    email_data = adminEmail.objects.get_or_create(id=1)
   
    return render(request, 'admin_email_view.html', {'email_data':email_data})

def admin_email_update(request):
    if 'admin_session_id' not in request.session:
        return redirect(login)

    receive_email = request.POST["receive_email"]
    from_email = request.POST["from_email"]
    
    email_data = adminEmail.objects.get_or_create(id=1)[0]
    email_data.receive_email = receive_email
    email_data.from_email = from_email
    email_data.save(update_fields=['receive_email', 'from_email'])

    messages.info(request,'Email Successfully Updated!')

    return redirect(admin_email_view)


class GrowerListView(generics.GenericAPIView, mixins.ListModelMixin,
											  mixins.CreateModelMixin,
											  mixins.RetrieveModelMixin,
											  mixins.UpdateModelMixin,
											  mixins.DestroyModelMixin):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	lookup_field = 'id'

	def get(self, request,id=None):
		print('id :inside mixin',id)
		if id:
			return self.retrieve(request, id)
		else:
			return self.list(request)

	def post(self, request):
		return self.create(request)

	def perform_create(self, serializer):
		serializer.save(created_date=datetime.now())

	def put(self, request, id=None):
		return self.update(request,id)

	def delete(self, request, id=None):
		return self.destroy(request,id)
