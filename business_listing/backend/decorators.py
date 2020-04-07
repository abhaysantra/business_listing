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

# def unauthenticated_user(view_func):
# 	def wrapper_func(request, *args, **kwargs):
# 		if request.user.is_authenticated:
# 			return redirect('home')
# 		else:
# 			return view_func(request, *args, **kwargs)

# 	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			print('Loggediin user type= %s and allowed type= %s' %(group,allowed_roles))
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page. Accessible to => %s'%(allowed_roles))
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		print('user group : ',group)
		if group == 'customer':
			return redirect('admin_index')
		if group == 'vendor':
			return redirect('admin_index')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function