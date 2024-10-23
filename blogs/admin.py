from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['author' , 'title'  , 'created_date' , 'published_date']
admin.site.register(Post , PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post' , 'author' ,'text' , 'created_date']
admin.site.register(Comment , CommentAdmin)

  