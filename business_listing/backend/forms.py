 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms

from .models import User, Book, MyUser #Order


# class OrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = MyUser
		# fields = ['username', 'email', 'password1', 'password2','user_type_id']
		fields = ['username', 'email', 'phone_number','password1', 'password2']

class UpdateUserForm(ModelForm):
	class Meta:
		model = MyUser
		fields = ['first_name', 'last_name','phone_number','picture']
		# exclude = ('password1','password2','user_type_id')

# class CreateUserForm(ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ['user_type_id','full_name', 'login_email']

class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = ['title','author', 'pdf','cover']