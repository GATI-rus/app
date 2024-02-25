from django.urls import path
from users import views
from .views import google_login

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
    # path('google/', views.login, name='google')
    path('login/', google_login, name='google_login'),
]
