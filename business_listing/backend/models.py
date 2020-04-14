from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class MyUser(AbstractUser):
    # user_type_id => 1-> Admin 2-> Agent 3-> Vendor 4-> Customer
    user_type_id = models.IntegerField(null=True)
    is_individual_vendor = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=255, null=True)
    created_date = models.DateField(auto_now_add = True, null=True)
    modified_date = models.DateField( null=True)

    uuid_code = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    
    
class MyUserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True)
    
    country = models.IntegerField(null=True)
    state = models.IntegerField(null=True)
    city = models.IntegerField(null=True)
    landmark = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    # address = models.TextField(null=True)
    pincode = models.CharField(max_length=255,null=True)
    picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    created_date = models.DateField(auto_now_add = True, null=True)
    modified_date = models.DateField( null=True)

    def __str__(self):
        return self.user.first_name

class VendorList(models.Model):
    agent = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)    
    vendor_id = models.IntegerField(null=True)

# customed Model Manager
class ParlourManager(models.Manager):
    def check_phonenumber(self, phone_number):
        if len(phone_number) == 10:
            return 'phone_number is correct'

        else:
            return 'Please check phone number'

class ParlourQuerySet(models.QuerySet):
    def check_phonenumber(self, phone_number):
        if len(phone_number) == 10:
            return 'phone_number is correct'

        else:
            return 'Please check phone number'          

# Create your models here.
class Parlour(models.Model):
    vendor = models.ForeignKey(MyUser,related_name='vendor', on_delete=models.CASCADE, null=True)
    agent = models.ForeignKey(MyUser, related_name='agent',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    landmark = models.CharField(max_length=255,null=True)
    country = models.IntegerField(null=True)
    state = models.IntegerField(null=True)
    city = models.IntegerField(null=True)
    pincode = models.CharField(max_length=255,null=True)
    picture = models.ImageField(upload_to='parlour/profile/', null=True, blank=True)

    status = models.CharField(max_length=10, default='active')
    created_date = models.DateField(auto_now_add = True, null=True)
    created_by = models.IntegerField(null=True)
    modified_date = models.DateField(null=True)
    modified_by = models.IntegerField(null=True)

    uuid_code = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    # objects = ParlourManager()
    parman = ParlourQuerySet()

      
    def __str__(self):
        return self.name

class ParlourService(models.Model):
    parlour = models.ForeignKey(Parlour,related_name='parlour', on_delete=models.CASCADE, null=True)
    service_name = models.CharField(max_length=255, null=True)
    service_duration= models.CharField(max_length=255, null=True)
    service_price = models.FloatField(default=0.0, null=True)
    service_material= models.TextField(null=True)

    status = models.CharField(max_length=10, default='active')
    created_date = models.DateField(auto_now_add = True, null=True)
    modified_date = models.DateField(null=True)

    uuid_code = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)


    # def __init__(self):
    #      super(Paid, self).__init__()
    #      self.uuid_code = str(uuid.uuid4())

    # this needs to be corrected
    def get_absolute_url(self):
        return "/path/%s/" %(self.uuid_code)

    def __str__(self):
        return self.service_name

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

class Countries(models.Model):
    country_id = models.IntegerField(null=True)
    sortname = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=250, null=True)
    phonecode = models.IntegerField(null=True)

    objects = models.Manager() # read docs


class States(models.Model):
    state_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    country_id = models.IntegerField(null=True)

    objects = models.Manager() # read docs

class Cities(models.Model):
    city_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    state_id = models.IntegerField(null=True)

    objects = models.Manager() # read docs


