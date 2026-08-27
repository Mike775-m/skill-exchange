from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)

from .forms import SkillForm, SkillSearchForm
from .models import Skill, Category, Favorite


class HomeView(TemplateView):
    """Modern landing page with hero section + latest skills preview."""
    template_name = 'skills/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_skills'] = Skill.objects.filter(is_active=True).select_related('category', 'owner')[:6]
        context['categories'] = Category.objects.all()[:8]
        context['total_skills'] = Skill.objects.filter(is_active=True).count()
        context['total_users'] = Skill.objects.values('owner').distinct().count()
        context['total_categories'] = Category.objects.count()
        return context


class SkillListView(ListView):
    model = Skill
    template_name = 'skills/skill_list.html'
    context_object_name = 'skills'
    paginate_by = 10

    def get_queryset(self):
        queryset = Skill.objects.filter(is_active=True).select_related('category', 'owner')
        self.form = SkillSearchForm(self.request.GET or None)

        query = self.request.GET.get('q', '').strip()
        category_slug = self.request.GET.get('category', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(category__name__icontains=query) |
                Q(description__icontains=query)
            )
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')

        if self.request.user.is_authenticated:
            context['favorited_ids'] = set(
                Favorite.objects.filter(user=self.request.user).values_list('skill_id', flat=True)
            )
        else:
            context['favorited_ids'] = set()
        return context


class SkillDetailView(DetailView):
    model = Skill
    template_name = 'skills/skill_detail.html'
    context_object_name = 'skill'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user, skill=self.object
            ).exists()
        else:
            context['is_favorited'] = False
        return context


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Your skill listing has been created!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context


class SkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_form.html'

    def test_func(self):
        return self.get_object().owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your skill listing has been updated!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context


class SkillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Skill
    template_name = 'skills/skill_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.get_object().owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'The skill listing has been deleted.')
        return super().form_valid(form)


@login_required
def dashboard(request):
    my_skills = Skill.objects.filter(owner=request.user).select_related('category')
    total_skills = Skill.objects.filter(is_active=True).count()
    my_favorites = Favorite.objects.filter(user=request.user).select_related('skill')

    return render(request, 'skills/dashboard.html', {
        'my_skills': my_skills,
        'total_skills': total_skills,
        'my_skill_count': my_skills.count(),
        'my_favorites': my_favorites,
    })


@login_required
def toggle_favorite(request, slug):
    skill = get_object_or_404(Skill, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, skill=skill)
    if not created:
        favorite.delete()
        messages.info(request, f'Removed "{skill.title}" from your favorites.')
    else:
        messages.success(request, f'Added "{skill.title}" to your favorites!')

    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('skill-detail', slug=skill.slug)
