from .models import Genre


def nav_genres(request):
    return {"genres": Genre.objects.order_by("name")}
