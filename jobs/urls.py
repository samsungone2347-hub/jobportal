from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('post-job/', views.post_job, name='post_job'),
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker-dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('job/<int:pk>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
]
