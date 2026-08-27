# Community Skill Exchange

A small Django app for trading skills locally — post what you're good at,
browse what other people are offering, no money involved.

Built this as a portfolio project to practice Django CRUD, auth, and a bit
of frontend polish with Bootstrap.

## Features

- Sign up / log in, edit your profile (bio, picture, location)
- Post skill listings with a category, description, location, contact info
- Search and filter listings, paginated
- Dashboard to manage your own listings
- Favorite skills you're interested in
- Dark mode toggle
- Django admin for managing everything

## Setup

```bash
git clone https://github.com/Mike775-m/community-skill-exchange.git
cd community-skill-exchange
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8001

Optional demo data:
```bash
python manage.py shell < seed_data.py
```

## Stack

Django, SQLite, Bootstrap 5, Pillow for image uploads.

