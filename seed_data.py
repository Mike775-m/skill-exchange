"""
Quick seed script for demo/testing purposes.
Run with: python manage.py shell < seed_data.py
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from skills.models import Category, Skill

categories_data = [
    ("Graphic Design", "bi-palette2"),
    ("Web Development", "bi-code-slash"),
    ("Tutoring", "bi-mortarboard"),
    ("Photography", "bi-camera"),
    ("Home Repair", "bi-tools"),
    ("Cooking", "bi-egg-fried"),
    ("Music Lessons", "bi-music-note-beamed"),
    ("Language Exchange", "bi-translate"),
]

for name, icon in categories_data:
    Category.objects.get_or_create(name=name, defaults={"icon": icon})

demo_user, created = User.objects.get_or_create(
    username="MIKE",
    defaults={"first_name": "michael", "last_name": "ngigi", "email": "michael@gmail.com"},
)
if created:
    demo_user.set_password("michael5482")
    demo_user.save()

sample_skills = [
    ("Logo & Brand Identity Design", "Graphic Design", "I design clean, modern logos and brand kits for small businesses and startups."),
    ("Beginner Python Tutoring", "Tutoring", "One-on-one Python lessons for absolute beginners, from syntax to small projects."),
    ("Portrait & Event Photography", "Photography", "Available for weddings, birthdays, and portrait sessions around the city."),
    ("React & Django Web Apps", "Web Development", "I build full-stack web applications using React and Django REST Framework."),
    ("Leaky Faucet & Small Repairs", "Home Repair", "Friendly neighbor who can fix small plumbing and household issues."),
    ("Guitar Lessons for Beginners", "Music Lessons", "Learn acoustic guitar basics, chords, and your favorite songs."),
]

for title, cat_name, desc in sample_skills:
    category = Category.objects.filter(name=cat_name).first()
    Skill.objects.get_or_create(
        title=title,
        defaults={
            "owner": demo_user,
            "description": desc,
            "category": category,
            "location": "Nairobi, Kenya",
            "contact_info": "michael@gmail.com",
        },
    )

print("Seed data created successfully.")
