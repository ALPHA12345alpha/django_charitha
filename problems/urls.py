from django.urls import path
from .views import ProblemListView, ProblemDetailView, ProblemCreateView, leaderboard

urlpatterns = [
    path('', ProblemListView.as_view(), name="problem_list"),
    path('<int:pk>/', ProblemDetailView.as_view(), name="problem_detail"),
    path('create/', ProblemCreateView.as_view(), name="problem_create"),
    path('leaderboard/', leaderboard, name="leaderboard"),
]
