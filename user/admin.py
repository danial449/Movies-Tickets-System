from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class User_Admin(UserAdmin):
    list_display = ('id', 'first_name', 'email' , 'is_staff')
    
    fieldsets = UserAdmin.fieldsets + (  # Include 'gender' in the 'Personal Information' section
        ('Other Information', {
            'fields': ('is_email_verified',),
        }),
    )
admin.site.register(User , User_Admin)


class Contact_Us_Admin(admin.ModelAdmin):
    list_display = ('id','first_name' , 'email' ,'message')
admin.site.register(ContactUs , Contact_Us_Admin)