from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home-page'),
    path('genre/<int:genre_id>/', views.books_by_genre, name='genre-books'),
    path('register/',views.register, name='register'),
    path('login/',views.loginUser, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('bookdetails/', views.bookDetails, name='book-details'),
    path('addtocart/<int:id>', views.add_to_cart, name='addtocart'),
    path('cart/', views.view_cart, name='crtpage'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
