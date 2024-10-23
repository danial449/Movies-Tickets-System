from django.db import models
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField
# Create your models here.
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True , null=True)
    post_image = models.ImageField(upload_to='post_featured_pics/' , null=True , blank=True)
    text = HTMLField(null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post , related_name='comments' , on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text
    