# GitHub Profile Viewer

A Django app that searches GitHub users through the public GitHub REST API,
shows their profile and recent repositories, and lets logged-in users
bookmark profiles.

## Run it
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000/

## Features
- Search a GitHub username (profile and 10 latest repos)
- Friendly messages for not found, rate limit, timeout and no connection
- Bookmark profiles (login required, no duplicates, POST only)
- Bookmarks page with remove button (users see only their own)
- Admin page for bookmarks
