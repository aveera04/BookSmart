from .models import Genre, CartItem


def nav_genres(request):
    return {"genres": Genre.objects.order_by("name")}

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    return {'cart_item_count': count}
