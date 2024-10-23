from django.urls import path
from .views import *

app_name = 'blogs'

urlpatterns =[
  path("blogs/", blog_view, name="blog"),
  path('details/<int:pk>/', post_details , name='post_details')
]