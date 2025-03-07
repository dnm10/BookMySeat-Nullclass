BookMySeat 🎟️

BookMySeat is a movie ticket booking web application built with Django. It allows users to browse movies, select theaters, choose seats, and book tickets — just like BookMyShow! The app also provides movie recommendations based on the genres users have previously watched.

🚀 Features

Movie Listings: Browse and search for movies.

Theater Management: View available theaters for each movie.

Seat Selection: Choose seats with live availability.

Booking System: Book tickets and get a confirmation email.

Recommendations: Get personalized movie recommendations based on previous bookings.

User Authentication: Login and registration system for secure bookings.

🛠️ Tech Stack

Backend: Django, Python

Frontend: HTML, CSS, Bootstrap

Database: SQLite (can be swapped for PostgreSQL or MySQL)

Email Service: Django's built-in email system (configurable with SMTP)

🛠️ Installation & Setup

Clone the repository:
git clone https://github.com/yourusername/BookMySeat.git
cd BookMySeat

Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Set up the database:
python manage.py makemigrations
python manage.py migrate

Create a superuser (for admin panel):
python manage.py createsuperuser

Run the development server:
python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser.

🚨 How to Use

Add movies and theaters: Log in to the Django admin panel at /admin and create movie entries, theaters, and seats.

Book a seat: Choose a movie, select a theater and showtime, and pick your seats.

Get recommendations: After booking a movie, check your profile page for recommended movies based on the genre you watched.
