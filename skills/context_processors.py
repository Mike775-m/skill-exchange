from .models import Category


def categories_processor(request):
    """Makes the full category list available to every template (used in navbar)."""
    return {'nav_categories': Category.objects.all()}
