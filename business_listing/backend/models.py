from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    user_type_id = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    address = models.TextField(null=True)
    

# Create your models here.
class User(models.Model):
# class User(AbstractUser):
    user_type_id = models.IntegerField()
    full_name = models.CharField(max_length=255)
    login_password = models.CharField(max_length=255)
    login_email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)


    gst_no = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=8, default='active')
    created_date = models.DateField(null=True)
    created_by = models.IntegerField(null=True)
    modified_date = models.DateField(null=True)
    modified_by = models.IntegerField(null=True)
    pin_code = models.CharField(max_length=255,null=True)
    country = models.IntegerField(null=True)
    state = models.IntegerField(null=True)
    city = models.IntegerField(null=True)

    landmark = models.CharField(max_length=255,null=True)
    # profile_image = models.ImageField(upload_to='user_profile' , null=True) #size=[150, 150] ,
    address = models.TextField(null=True)
      
    def __str__(self):
        return self.full_name

# to recieive email from business owners
class adminEmail(models.Model):
    receive_email = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)       

    def __str__(self):
        return self.from_email

class VendorInfo(models.Model):
    myuser = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    info = models.TextField(null=True)
    service = models.TextField(null=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    # for file uploading  
    pdf = models.FileField(upload_to='Books/pdf/') 
    # for image uploading  
    cover = models.ImageField(upload_to='Books/cover/', null=True, blank=True)     

    def __str__(self):
        return self.from_email


