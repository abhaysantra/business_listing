from django.urls import path
from backend.views import *

urlpatterns = [
    
    path('getGrowerList/', GrowerListView.as_view()),

    path('', index, name='admin_index'),
    path('login/', loginUser, name='login'),
    path('login_action/', login_action, name='login_action'),
    path('logout/', logoutUser, name='logout'),

    #-------------- based on form --------------------#
    path('registerpage/', registerPage, name='registerpage'),
    path('updateprofile/<int:pk>/', updateProfile, name='updateprofile'),

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