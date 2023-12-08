
from django.contrib.auth.models import AbstractUser
from django.db import models



class RoleMaster(models.Model):
    role_name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)  
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.CharField(max_length=150,null=True)
    modified_by = models.CharField(max_length=150,null=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'rolemaster'




class Customuser(AbstractUser):
    first_name = models.CharField(max_length=20,null=True)
    last_name = models.CharField(max_length=20,null=True)
    username = models.CharField(null=True,unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(unique=True,null=True)
    country_code = models.CharField(max_length=10,null=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(null=True)
    country_name = models.CharField(max_length=50,null=True)
    state_name = models.CharField(max_length=50,null=True)
    zipcode = models.IntegerField(null=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    bio = models.CharField(max_length=256,null=True)
    date_of_birth = models.DateField(null=True)
    temp_otp = models.CharField(max_length=6)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    is_delete = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(RoleMaster, on_delete=models.SET_NULL, null=True, related_name='created_users')
    modified_by = models.ForeignKey(RoleMaster, on_delete=models.SET_NULL, null=True, related_name='modified_users')


    class Meta:
        ordering = ['-created_at']
        db_table = 'customuser'
