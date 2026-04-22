from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home-page'),
    path('register/',views.register, name='register'),
    path('login/',views.loginUser, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('bookdetails/', views.bookDetails, name='book-details'),
]
