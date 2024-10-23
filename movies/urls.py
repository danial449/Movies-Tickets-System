from django.urls import path
from .views import *

app_name = 'movies'

urlpatterns =[
  path("movies/", movie_view, name="movie"),
  path('movie/<int:movie_id>/<str:category>/', single_movie_view, name='single_movie'),
  path('book-ticket/<str:movie_name>/', book_ticket, name='book_ticket'),
  path('payment/<int:ticket_id>/', payment_view, name='payment'),
  path('tickets/', tickets_view, name='ticket'),
  path('search/', movie_search, name='movie_search'),
]