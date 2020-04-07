from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		print('decorator called :',request.user)
		if 'admin_session_id' in request.session:
			return view_func(request, *args, **kwargs)
			
		else:
			return redirect('login')

	return wrapper_func