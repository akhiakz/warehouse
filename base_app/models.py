from sre_parse import State
from django.db import models
from django.conf import settings

         
class user_registration(models.Model):
     firstname = models.CharField(max_length=255, null=True)
     lastname = models.CharField(max_length=255, null=True)
     username = models.CharField(max_length=255, null=True)
     password = models.CharField(max_length=255, null=True)
     cpassword = models.CharField(max_length=255, null=True)
     joiningdate = models.DateField(
        auto_now_add=False, auto_now=False,  null=True, blank=True)

class department(models.Model):
     department_name = models.CharField(max_length=100)

class staff_registration(models.Model):
     department = models.ForeignKey(department, on_delete=models.DO_NOTHING,null=True, blank=True) 
     fullname = models.CharField(max_length=255, null=True, )
     email = models.EmailField(max_length=255, null=True,)
     mobile = models.CharField(max_length=240, null=True)
     password = models.CharField(max_length=255, null=True,)
     photo = models.FileField(default='blank.jpg', upload_to='images/', null=True, blank=True)
     dateofbirth = models.DateField(
        auto_now_add=False, auto_now=False,  null=True, blank=True)
     joiningdate = models.DateField(
        auto_now_add=False, auto_now=False,  null=True, blank=True)
     address1 = models.CharField(max_length=240, null=True)
     address2 = models.CharField(max_length=240, null=True)
     pincode = models.CharField(max_length=240, null=True)
     district = models.CharField(max_length=240, null=True)
     State = models.CharField(max_length=240, null=True)
     salary = models.CharField(max_length=200)
     status = models.CharField(max_length=255, null=True)

class order_request(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,null=True, blank=True) 
     staff = models.ForeignKey(staff_registration, on_delete=models.DO_NOTHING,null=True, blank=True) 
     firstname = models.CharField(max_length=255, null=True)
     lastname = models.CharField(max_length=255, null=True)
     email = models.EmailField(max_length=255, null=True)
     companyname = models.CharField(max_length=255, null=True)
     producttype = models.CharField(max_length=255, null=True)
     quantity = models.IntegerField(default='0')
     timetocontact = models.CharField(max_length=255, null=True)
     tranporttype = models.CharField(max_length=255, null=True)
     messege = models.CharField(max_length=255, null=True)
     status = models.CharField(max_length=255, null=True)
     reject_reason = models.CharField(max_length=255, null=True)
     rate = models.CharField(max_length=200)
     shipmentdate = models.DateField(
        auto_now_add=False, auto_now=False,  null=True, blank=True)
     from_place = models.CharField(max_length=255, null=True)
     to_place = models.CharField(max_length=255, null=True)
     tracking_status = models.CharField(max_length=255, null=True)
     shipment_status = models.CharField(max_length=255, null=True)
     expected_date = models.DateField(
        auto_now_add=False, auto_now=False,  null=True, blank=True)
     
class payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,null=True, blank=True)                        
    order = models.ForeignKey(order_request, on_delete=models.DO_NOTHING,null=True, blank=True)                        
    date = models.DateField(auto_now_add=False, auto_now=False,  null=True, blank=True)
    payment = models.CharField(max_length=240, null=True)
    bank = models.CharField(max_length=240, null=True)
    accountnumber = models.CharField(max_length=240, null=True)
    ifse = models.CharField(max_length=240, null=True)
