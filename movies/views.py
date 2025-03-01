from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Count


def movie_list(request):
    search_query = request.GET.get('search')
    movies = Movie.objects.all()
    recommendations = []

    if search_query:
        movies = movies.filter(name__icontains=search_query)
    
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user=request.user)
        watched_genres = user_bookings.values_list('movie__genre', flat=True).distinct()
        
        # Fetch genres from the related movies
        watched_genres = user_bookings.values_list('movie__genre', flat=True).distinct()
        
        if watched_genres:
            recommendations = Movie.objects.filter(genre__in=watched_genres).exclude(id__in=user_bookings.values_list('movie_id', flat=True))

        # Print to debug
        print(f"Watched genres: {watched_genres}")
        print(f"Recommended movies: {recommendations}")

    return render(request, 'movies/movie_list.html', {'movies': movies, 'recommendations': recommendations})



def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})



@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theaters = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theaters)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []
        booked_seats = []

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                'theaters': theaters,
                "seats": seats,
                'error': "No seat selected"
            })

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theaters)

            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue

            try:
                booking = Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )

                seat.is_booked = True
                seat.save()

                booked_seats.append(booking)

            except IntegrityError:
                error_seats.append(seat.seat_number)

        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {
                'theaters': theaters,
                "seats": seats,
                'error': error_message
            })

        # Send confirmation email
        send_booking_confirmation_email(booked_seats, request.user)

        messages.success(request, 'Your seats have been successfully booked! Check your email for details.')
        return redirect('profile')

    return render(request, 'movies/seat_selection.html', {'theaters': theaters, "seats": seats})


def send_booking_confirmation_email(bookings, user):
    if not bookings:
        return

    subject = 'Booking Confirmation - Your Movie Tickets'
    seat_numbers = ', '.join([booking.seat.seat_number for booking in bookings])
    theater_name = bookings[0].theater.name
    movie_name = bookings[0].movie.name
    show_time = bookings[0].theater.time.strftime('%Y-%m-%d %H:%M')

    message = f"""
Hello {user.username},

Your booking is confirmed!

Movie: {movie_name}
Theater: {theater_name}
Show Time: {show_time}
Seat Numbers: {seat_numbers}

Thank you for booking with us!

Regards,
Movie Ticket Booking Team
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
