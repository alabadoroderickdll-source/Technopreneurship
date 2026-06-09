from django.contrib import admin
from .models import (UserProfile, Resume, Education, Experience, Skill,
                     Certification, Job, JobApplication, InterviewSession,
                     InterviewQuestion, InterviewAnswer, ContactMessage)

admin.site.site_header = "CareerSync Admin"
admin.site.site_title = "CareerSync"
admin.site.index_title = "Welcome to CareerSync Admin"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'full_name', 'score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'user__username']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['school', 'degree', 'resume']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'resume']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'resume']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'category', 'job_type', 'is_active', 'created_at']
    list_filter = ['category', 'job_type', 'is_active']
    search_fields = ['title', 'company']
    list_editable = ['is_active']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status']

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'score', 'completed', 'created_at']

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'submitted_at']
    list_filter = ['is_read']
    list_editable = ['is_read']
