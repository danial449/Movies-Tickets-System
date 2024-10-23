from django.contrib import admin
from .models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'category')
    list_filter = ('category',) 
    search_fields = ('title',) 
    ordering = ('title',)  

admin.site.register(Movie, MovieAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_name')

admin.site.register(Ticket, TicketAdmin)
