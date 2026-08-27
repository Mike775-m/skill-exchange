from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    path('skills/new/', views.SkillCreateView.as_view(), name='skill-create'),
    path('skills/<slug:slug>/', views.SkillDetailView.as_view(), name='skill-detail'),
    path('skills/<slug:slug>/edit/', views.SkillUpdateView.as_view(), name='skill-update'),
    path('skills/<slug:slug>/delete/', views.SkillDeleteView.as_view(), name='skill-delete'),
    path('skills/<slug:slug>/favorite/', views.toggle_favorite, name='skill-favorite'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
