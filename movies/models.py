from django.db import models
from user.models import User
# Create your models here.

class Movie(models.Model):
    CATEGORY_CHOICES = [
        ('popular', 'Popular'),
        ('upcoming', 'Upcoming'),
        ('now_playing', 'Now Playing'),
        ('top_rated', 'Top Rated'),
    ]

    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    poster_url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=255)
    booking_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=150)
    payment_status = models.BooleanField(default=False)
    seat_no = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie_name}"