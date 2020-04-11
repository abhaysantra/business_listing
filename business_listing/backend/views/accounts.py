from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import datetime
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



# Create your views here.
from backend.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from backend.models import *
from backend.decorators import *
from backend.forms import *

# source link : https://github.com/maxg203/Django-Tutorials/blob/master/accounts/templates/accounts/change_password.html
# for change_password : https://www.youtube.com/watch?v=QxGKTvx-Vvg

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #to set user_type id 1=> superuser 2=> vendor 3=> customer
            group = Group.objects.get(name='vendor')
            user.groups.add(group)
            user.user_type_id = 2
            user.save()
            #user profile to be created with empty data
            obj = MyUserProfile(user=user)
            obj.save()
            messages.success(request, 'Account was created with : ' + username)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'account/register.html', context)

# @unauthenticated_user
# @login_required(login_url='login')
# @admin_only
@login_required()
def updateProfile(request, pk):
    user = MyUser.objects.get(id=pk)
    myProfile = MyUserProfile.objects.get(user=user)
    if request.method == 'POST':
        userform = UpdateUserForm(request.POST,request.FILES, instance=user)
        userProfileForm = UpdateUserProfileForm(request.POST,request.FILES,instance=myProfile)
        if userform.is_valid() and userProfileForm.is_valid():
            userform.save()
            userProfile = userProfileForm.save(commit=False)
            userProfile.modified_date = datetime.now()
            userProfile.save()
            return redirect('admin_index')

    userform = UpdateUserForm(instance=user)
    profileform = UpdateUserProfileForm(instance=myProfile)
    context = {'form':userform,'profileform':profileform}
    return render(request, 'edit_profile_using_form.html', context)

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(index)
        else:
            form = PasswordChangeForm(user=request.user)
            args = {'form': form}
            return render(request, 'account/change_password.html', args)
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'account/change_password.html', args)


#-------- upload book with FIle and Image field -------------#
@login_required(login_url='login')
@allowed_users(allowed_roles=['vendor'])
def upload_book(request):
    book_form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, 'Book uploaded title: ' + title)

            return redirect('book_list')

    return render(request,'book/upload_book.html',{'form':book_form}) 

@login_required()
def book_list(request):
    books= Book.objects.all()
    return render(request,'book/book_list.html',{'books':books})   

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_book(request,id):
    book = Book.objects.get(id=id)
    book_form = BookForm(instance=book)

    print('request.method :',request.method)
    if request.method == 'POST':
        # form = BookForm(request.POST, instance=user)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, 'Book updated for :' + title)

            return redirect('book_list')

    return render(request,'book/update_book.html',{'form':book_form}) 

@login_required(login_url='login')
def delete_book(request, id):
    book = Book.objects.get(id=id)
    # if request.method == "POST":
    if request.method == "GET":
        book.delete()
        return redirect('book_list')

    return render(request, 'book/book_list.html',{'form':Book.objects.all()})

#-----------------------end-----------------------------------#




def loginUser(request):
    return render(request, 'account/login.html')

def login_action(request):
    login_email = request.POST["login_email"] # instead of email make it username as username is unique in DB
    # login_email = request.POST["login_email"]
    login_password = request.POST["login_password"] 
    print(login_email,login_password)

    #test authenticate
    user = authenticate(request, username=login_email,password=login_password)
    print('authenticate :',user)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['admin_session_id'] = user.id
            request.session['admin_session_name'] = user.username
            return redirect(index)
        else:
            messages.error(request,'Inactive User Please check !!!')
            return redirect(loginUser)
    else:
        messages.error(request,'username or password not correct')
        return redirect(loginUser)  

def logoutUser(request):
    if 'admin_session_id' in request.session:
        del request.session['admin_session_id']
        del request.session['admin_session_name']
    messages.info(request,'Successfully Logged out!')
    logout(request)
    
    return redirect(loginUser)

@login_required()
def index(request):

    context = {
        'vendorCounter':MyUser.objects.filter(user_type_id=2).count(),
    }
    return render(request, 'dashboard_view.html', context)

# @unauthenticated_user
# @allowed_users(['admin'])
@admin_only
def admin_profile(request):
    if 'admin_session_id' not in request.session:
        return redirect(loginUser)

    admin_session_id = request.session['admin_session_id']
    profile_data = MyUser.objects.get(id=admin_session_id)
   
    return render(request, 'admin_profile_edit.html', {'profile_data':profile_data})

@admin_only
def admin_profile_edit(request):
    full_name = request.POST["full_name"]
    email = request.POST["email"]
    userid = request.POST["userid"]

    profile_data = User.objects.get(id=userid)
    profile_data.full_name = full_name
    profile_data.login_email = email
    profile_data.save(update_fields=['full_name', 'login_email'])

    messages.info(request,'Profile Successfully Updated!')

    return redirect(admin_profile)



################### to be removed #####################
@login_required
def admin_password_view(request):
    profile_data = MyUser.objects.get(id=request.user.id)
    return render(request, 'admin_password_change.html', {'profile_data':profile_data})

@login_required
def admin_password_update(request):

    con_pass = request.POST["con_pass"]
    hidden_user_id = request.POST["hidden_user_id"]
    
    adminObj = MyUser.objects.get(id=hidden_user_id)
    adminObj.password = con_pass
    adminObj.save(update_fields=['login_password'])

    messages.info(request,'Password Successfully Updated!')

    return redirect(admin_password_view)

##################################################

@login_required
def admin_email_view(request):
    email_data = adminEmail.objects.get_or_create(id=request.user.id)
   
    return render(request, 'admin_email_view.html', {'email_data':email_data})

def admin_email_update(request):
    if 'admin_session_id' not in request.session:
        return redirect(loginUser)

    receive_email = request.POST["receive_email"]
    from_email = request.POST["from_email"]
    
    email_data = adminEmail.objects.get(id=1)
    email_data.receive_email = receive_email
    email_data.from_email = from_email
    email_data.save(update_fields=['receive_email', 'from_email'])

    messages.info(request,'Email Successfully Updated!')

    return redirect(admin_email_view)

##################################  TO BE REMOVED #########################


#################################################### using mixin  #####################
class GrowerListView(generics.GenericAPIView, mixins.ListModelMixin,
											  mixins.CreateModelMixin,
											  mixins.RetrieveModelMixin,
											  mixins.UpdateModelMixin,
											  mixins.DestroyModelMixin):
	serializer_class = MyUserSerializer
	queryset = MyUser.objects.all()
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
