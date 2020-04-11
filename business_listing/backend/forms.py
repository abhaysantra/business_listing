 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms

# from .models import User, Book, MyUser, MyUserProfile
from .models import *


# class OrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = MyUser
		fields = ['username', 'email', 'phone_number','password1', 'password2']

	def clean_email(self):
		user = self.cleaned_data['username']
		try:
			match = MyUser.objects.get(email=email)		
		except:
			raise forms.ValidationError(' email already exists!!!')
		return user

class UpdateUserForm(ModelForm):
	class Meta:
		model = MyUser
		fields = ['username','first_name','last_name', 'email', 'phone_number']

	def clean_username(self):
		user = self.cleaned_data['username']
		try:
			match = MyUser.objects.get(username=user)		
		except:
			raise forms.ValidationError(' Username already exists')
		return user

class UpdateUserProfileForm(ModelForm):
	class Meta:
		model = MyUserProfile
		# fields = '__all__'
		exclude = ('user','modified_date')

class VendorCreationForm(ModelForm):
	class Meta:
		model = MyUser
		fields = ['username', 'email', 'phone_number']

class VendorUpdateForm(ModelForm):
	class Meta:
		model = MyUser
		fields = ['username','first_name','last_name', 'email', 'phone_number']

class ParlourCreationForm(ModelForm):
	class Meta:
		model = Parlour
		exclude = ['agent', 'status', 'created_date','created_by','modified_date','modified_by']

class ParlourServiceCreationForm(ModelForm):
	class Meta:
		model = ParlourService
		exclude = ['parlour', 'status', 'created_date','modified_date']



# class CreateUserForm(ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ['user_type_id','full_name', 'login_email']

class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = ['title','author', 'pdf','cover']