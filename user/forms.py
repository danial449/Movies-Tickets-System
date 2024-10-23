from .models import *
from django import forms 
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True, widget=forms.TextInput(attrs = {"class":"form-control"}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))

class UserSignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','username', 'email' , 'password1')

    def clean_password2(self):
        # Override this method to prevent validation errors when password2 is not present
        return self.cleaned_data.get('password1')
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please choose another.")
        return email
    
class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactUs
        fields = "__all__"