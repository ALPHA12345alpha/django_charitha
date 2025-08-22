from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:problem_id>/', views.SubmissionCreateView.as_view(), name="submit_create"),
    path('<int:pk>/', views.SubmissionDetailView.as_view(), name="submission_detail"),
    path('status/<int:submission_id>/', views.submission_status, name="submission_status"),
    path('', views.SubmissionListView.as_view(), name="submission_list"),
    # Contest URLs
    path('contests/', views.ContestListView.as_view(), name="contest_list"),
    path('contests/<int:pk>/', views.ContestDetailView.as_view(), name="contest_detail"),
    path('contests/create/', views.ContestCreateView.as_view(), name="contest_create"),
]
