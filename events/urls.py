from django.urls import path
from .views import *

app_name = 'events'

urlpatterns =[
  path("events/", event_view, name="event"),
]