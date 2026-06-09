from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Resume
    path('resume/', views.resume_list, name='resume_list'),
    path('resume/create/', views.resume_create, name='resume_create'),
    path('resume/<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('resume/<int:pk>/preview/', views.resume_preview, name='resume_preview'),
    path('resume/<int:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('resume/<int:pk>/analyze/', views.resume_analyze, name='resume_analyze'),

    # Jobs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', views.job_apply, name='job_apply'),
    path('my-applications/', views.my_applications, name='my_applications'),

    # Interview
    path('interview/', views.interview_home, name='interview_home'),
    path('interview/start/', views.interview_start, name='interview_start'),
    path('interview/<int:session_id>/question/', views.interview_question, name='interview_question'),
    path('interview/<int:session_id>/results/', views.interview_results, name='interview_results'),

    # Recruiter
    path('recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/post/', views.recruiter_post_job, name='recruiter_post_job'),
    path('recruiter/jobs/<int:job_id>/applicants/', views.recruiter_applicants, name='recruiter_applicants'),
]
