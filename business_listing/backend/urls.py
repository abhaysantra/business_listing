from django.urls import path
from backend.views import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    
    path('getGrowerList/', GrowerListView.as_view()),

    path('testoauth', TemplateView.as_view(template_name="account/login11.html")),
    path('', index, name='admin_index'),
    path('login/', loginUser, name='login'),
    path('login_action/', login_action, name='login_action'),
    path('logout/', logoutUser, name='logout'),

    # t have state and city list based on country
    path('get_state_list/', get_state_list, name='get_state_list'),
    path('get_city_list/', get_city_list, name='get_city_list'),

    #-------------- based on form --------------------#
    path('registerpage/', registerPage, name='registerpage'),
    path('updateprofile/<int:pk>/', updateProfile, name='updateprofile'),
    path('change_password/', change_password, name='change_password'),

    ############# forgot password and reset password ----###########################
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), 
        name="password_reset_complete"),

    ###################################### Forgot and Reset Password done #############


    # Agent section 
    path('agentlist/', agentList, name='agentList'),
    path('getvendorlist/<int:id>', getVendorList, name='getvendorlist'),

    # now Agent can add vendor to his vendor list
    path('addvendor/', addVendor, name='addvendor'),
    # Indivudual vendor list who are not under any agent
    path('individual_vendor_list/', individual_vendor_list, name='individual_vendor_list'),

    ########### Parlour section ############
    path('list_parlour/', list_parlour, name='list_parlour'),
    path('add_parlour/', add_parlour, name='add_parlour'),
    path('edit_parlour/<int:id>/', edit_parlour, name='edit_parlour'),
    path('delete_parlour/<int:id>/', delete_parlour, name='delete_parlour'),
    path('change_status/', change_status, name='change_status'),

    ########### Parlour service section ############
    path('list_parlour_service/<int:parlour_id>/', list_parlour_service, name='list_parlour_service'),
    path('add_parlour_service/', add_parlour_service, name='add_parlour_service'),
    path('edit_parlour_service/<int:id>/', edit_parlour_service, name='edit_parlour_service'),
    path('delete_parlour_service/<int:id>/', delete_parlour_service, name='delete_parlour_service'),
    path('change_status_parlour_service/', change_status_parlour_service, name='change_status_parlour_service'),
    

    # TO UPLOAD AND DISPALY BOOK
    path('books/', book_list, name='book_list'),
    path('books/upload/', upload_book, name='upload_book'),
    path('books/update_book/<int:id>/', update_book, name='update_book'),
    path('books/delete_book/<int:id>/', delete_book, name='delete_book'),



    #-------------------------------------------------#

    path('admin_profile/', admin_profile, name='admin_profile'),
    path('admin_profile_edit/', admin_profile_edit, name='admin_profile_edit'),
    path('admin_password_view/', admin_password_view, name='admin_password_view'),
    path('admin_password_update/', admin_password_update, name='admin_password_update'),
    path('admin_email_view/', admin_email_view, name='admin_email_view'),
    path('admin_email_update/', admin_email_update, name='admin_email_update'),

]