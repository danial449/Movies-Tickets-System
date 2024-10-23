from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def blog_view(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context ={
        'posts': posts
    }
    return render(request , 'blogs/blogs.html' , context)


def post_details(request , pk):
    post = get_object_or_404(Post , pk=pk)
    recent_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:10]
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Submit Successfully! Thank you for your comment.")
            return redirect('blogs:post_details' , pk=post.pk)
    else:
        form=CommentForm()
    context = {
        'post':post , 
        'comments':comments, 
        'form':form,
        'recent_post':recent_post
    } 
    return render(request , 'blogs/post_details.html', context)