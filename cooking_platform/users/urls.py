from django.urls import path
from .views import register, custom_logout, profile, CustomLoginView

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
]