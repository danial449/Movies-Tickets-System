from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from  blogs.models import Post

# Your TMDb API key
TMDB_API_KEY = "055d2e889f8209142f2a35aed96bdceb"

# Base URL for TMDb images
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def movie_view(request):
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
    
    return render(request, 'movies/movies.html', context)

def single_movie_view(request, movie_id, category):
    # Define the category-based API URL
    category_apis = {
        'popular': f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}",
        'upcoming': f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}",
        'now_playing': f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}",
        'top_rated': f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}"
    }

    # Fetch movies based on the category
    response = requests.get(category_apis[category])
    movies = response.json().get('results', [])

    # Find the specific movie by ID within the category
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie is None:
        # You may want to handle the case where the movie is not found
        return render(request, "movies/movie_not_found.html", {"category": category})

    # Generate poster URL
    if 'poster_path' in movie:
        movie['poster_url'] = f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"

    # Context to pass to the template
    context = {
        'movie': movie,
    }
    
    return render(request, "movies/single-movie.html", context)

@login_required
def book_ticket(request, movie_name):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            # Get the next available seat
            existing_seats = Ticket.objects.filter(movie_name=movie_name).values_list('seat_no', flat=True)
            all_seats = set(range(1, 51))  # Assume total seats are from 1 to 50
            available_seats = all_seats - set(existing_seats)

            if not available_seats:
                return render(request, 'movies/tickets.html', {'error': 'No seats available', 'form': form})

            ticket = form.save(commit=False)
            ticket.user = request.user  # Associate the logged-in user
            ticket.movie_name = movie_name  # Set the movie name
            ticket.payment_status = False  # Set payment status to false initially
            ticket.seat_no = min(available_seats)  # Assign the lowest available seat number
            ticket.save()

            return redirect('movies:payment', ticket_id=ticket.id)
    else:
        form = TicketForm(initial={'movie_name': movie_name})
    
    return render(request, 'movies/tickets.html', {'form': form, 'movie_name': movie_name})


@login_required
def payment_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    if request.method == 'POST':
        # Update payment status to True
        ticket.payment_status = True
        ticket.save()
        # Redirect to the ticket slip page
        return redirect('movies:ticket')
    
    return render(request, 'movies/payment.html', {'ticket': ticket})

def tickets_view(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, "movies/tickets.html", {'tickets': tickets})


def movie_search(request):
    query = request.GET.get('query', '')  # Get the search query from the URL

    if query:
        # API URL for searching movies by query
        search_api_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
        response = requests.get(search_api_url)
        search_results = response.json().get('results', [])

        # Set the poster URL for each movie in the search results
        for movie in search_results:
            if 'poster_path' in movie:
                movie['poster_url'] = f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}"

        context = {
            'query': query,
            'search_results': search_results
        }
    else:
        context = {
            'query': '',
            'search_results': []
        }

    return render(request, 'movies/movie_search_results.html', context)