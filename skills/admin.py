from django.contrib import admin
from .models import Category, Skill, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'location', 'is_active', 'date_posted')
    list_filter = ('category', 'is_active', 'date_posted')
    search_fields = ('title', 'description', 'location', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_posted'
    list_editable = ('is_active',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'created_at')
    search_fields = ('user__username', 'skill__title')
