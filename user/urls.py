from django.urls import path
from .views import *

app_name = 'user'

urlpatterns =[
  path("", home_view, name="home"),
  path("about/", about_view, name="about"),
  path("faqs/", faqs_view, name="faqs"),
  path("contact/", contact_view, name="contact"),
  path("register/", user_register_view, name="register"),
  path("login/", user_login_view, name="login"),
  path("logout/", user_logout_view, name="logout"),
  path("verify_email/<str:token>/", verify_email_view, name="verify_email"),
  
]