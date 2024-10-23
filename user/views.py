from django.shortcuts import render , redirect 
from .models import User
from django.http import HttpResponse , JsonResponse
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import requests
from blogs.models import Post
from movies.models import *
# Create your views here.

# Your TMDb API key
TMDB_API_KEY = "055d2e889f8209142f2a35aed96bdceb"

# Base URL for TMDb images
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def home_view(request):
    blogs = Post.objects.all()[:2]
    # API URLs
    movie_api = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
    upcoming_movie_api = f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}"
    now_playing_movie_api = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}"
    top_rated_movie_api = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}"
    
    # Fetch data from each API
    popular_movies = requests.get(movie_api).json().get('results', [])
    upcoming_movies = requests.get(upcoming_movie_api).json().get('results', [])
    now_playing_movies = requests.get(now_playing_movie_api).json().get('results', [])
    top_rated_movies = requests.get(top_rated_movie_api).json().get('results', [])

    # Combine all movies into a single list
    all_movies = popular_movies + upcoming_movies + now_playing_movies + top_rated_movies

    # Set a maximum popularity value for percentage calculation
    max_popularity = max(movie['popularity'] for movie in all_movies if 'popularity' in movie) if all_movies else 1

    # Calculate poster URL and percentage popularity for each movie
    for movie in all_movies:
        if 'poster_path' in movie:
            movie['poster_url'] = f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"  # Full URL for poster

        if 'popularity' in movie:
            movie['popularity_percentage'] = (movie['popularity'] / max_popularity) * 100  # Calculate percentage

    # Context to pass to the template
    context = {
        'blogs' : blogs,
        'movies': popular_movies,
        'upcoming_movies': upcoming_movies,
        'now_playing_movies': now_playing_movies,
        'top_rated_movies': top_rated_movies
    }
    return render(request, 'user/home.html', context)

def about_view(request):
  return render(request, "user/about.html")

def faqs_view(request):
  return render(request, "user/faqs.html")

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been successfully submitted! We'll get back to you as soon as possible. Thank you for reaching out.")
            return redirect('user:contact')
        else:
            print(form.errors)
    else:
        form = ContactForm()
    return render(request  , 'user/contact.html' , {'form':form})

def user_register_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            password1 = form.cleaned_data.get('password1')
            user.set_password(password1)  # Properly set the hashed password
            user.is_staff = False  
            user.is_email_verified = False
            user.email_verification_token = str(uuid.uuid4())
            user.save()  # Save the user using the manager of your custom User model

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            activation_link = f'http://{current_site}/verify_email/{user.email_verification_token}/'
            message = f'Click the link to activate your account: {activation_link}'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "Thank you for registering! Please check your email to verify your account before logging in.")

            # Return success as JSON response
            return JsonResponse({'success': True})
        else:
            # Return form errors as JSON response
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    # If the request is not POST, render the registration form as usual
    form = UserSignUpForm()
    return render(request, "user/home.html", {'form': form})



def verify_email_view(request , token):
    try:
        user = User.objects.get(email_verification_token = token)
        if user:
           user.is_email_verified = True
           user.email_verification_token = None
           user.save()
           return redirect('user:home')
    except:
        return HttpResponse("Activation Link is Invalid")
    
def user_login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(email=email, password=password)

            if user is not None:
                # Check if the email is verified
                if user.is_email_verified:
                    login(request, user)
                    return redirect('user:home')
                else:
                    messages.error(request, 'Email not verified. Please check your email for verification link.')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')

        else:
            print(form.errors)  # Print form errors to the terminal for debugging
    else:
        form = LoginForm()

    return render(request, 'user/home.html', {'form': form})

def user_logout_view(request):
    logout(request)
    return redirect('user:home')