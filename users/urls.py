from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('profile/<str:username>/', views.profile, name="user_profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('toggle-theme/', views.toggle_theme, name="toggle_theme"),
    path('leaderboard/', views.leaderboard, name="user_leaderboard"),
]
