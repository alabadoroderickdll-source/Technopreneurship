from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
import random

from .models import (Resume, Education, Experience, Skill, Certification,
                     Job, JobApplication, InterviewSession, InterviewQuestion,
                     InterviewAnswer, ContactMessage, UserProfile)
from .forms import (RegisterForm, LoginForm, ResumeForm, EducationForm,
                    ExperienceForm, SkillForm, CertificationForm, JobForm,
                    JobApplicationForm, InterviewAnswerForm, ContactForm)


# ─── Public Pages ───────────────────────────────────────────────────────────

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    jobs_count = Job.objects.filter(is_active=True).count()

    # ✅ Add this line
    top_jobs = ["BPO Agent", "IT Support", "Remote Dev"]

    return render(request, 'core/landing.html', {
        'jobs_count': jobs_count,
        'top_jobs': top_jobs
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent successfully.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


# ─── Authentication ──────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to CareerSync, {user.first_name}!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'core/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('landing')


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    user = request.user
    resumes = Resume.objects.filter(user=user)
    applications = JobApplication.objects.filter(applicant=user)
    sessions = InterviewSession.objects.filter(user=user)
    recent_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]

    # Match jobs to best resume
    best_resume = resumes.first()
    matched_jobs = []
    for job in recent_jobs:
        pct = job.get_match_percent(best_resume)
        matched_jobs.append((job, pct))
    matched_jobs.sort(key=lambda x: x[1], reverse=True)

    context = {
        'resumes_count': resumes.count(),
        'applications_count': applications.count(),
        'sessions_count': sessions.count(),
        'matched_jobs': matched_jobs[:4],
        'recent_sessions': sessions.order_by('-created_at')[:3],
        'resumes': resumes[:3],
    }
    return render(request, 'core/dashboard.html', context)


# ─── Resume Builder ───────────────────────────────────────────────────────────

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'core/resume/list.html', {'resumes': resumes})


@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, "Resume created! Now add your education and experience.")
            return redirect('resume_edit', pk=resume.pk)
    else:
        user = request.user
        form = ResumeForm(initial={
            'full_name': user.get_full_name(),
            'email': user.email,
        })
    return render(request, 'core/resume/create.html', {'form': form})


@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume_form = ResumeForm(instance=resume)
    edu_form = EducationForm()
    exp_form = ExperienceForm()
    skill_form = SkillForm()
    cert_form = CertificationForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_resume':
            resume_form = ResumeForm(request.POST, instance=resume)
            if resume_form.is_valid():
                resume_form.save()
                messages.success(request, "Resume updated!")

        elif action == 'add_education':
            edu_form = EducationForm(request.POST)
            if edu_form.is_valid():
                edu = edu_form.save(commit=False)
                edu.resume = resume
                edu.save()
                messages.success(request, "Education added!")

        elif action == 'add_experience':
            exp_form = ExperienceForm(request.POST)
            if exp_form.is_valid():
                exp = exp_form.save(commit=False)
                exp.resume = resume
                exp.save()
                messages.success(request, "Experience added!")

        elif action == 'add_skill':
            skill_form = SkillForm(request.POST)
            if skill_form.is_valid():
                skill = skill_form.save(commit=False)
                skill.resume = resume
                skill.save()
                messages.success(request, "Skill added!")

        elif action == 'add_certification':
            cert_form = CertificationForm(request.POST)
            if cert_form.is_valid():
                cert = cert_form.save(commit=False)
                cert.resume = resume
                cert.save()
                messages.success(request, "Certification added!")

        elif action == 'delete_education':
            item_id = request.POST.get('item_id')
            Education.objects.filter(pk=item_id, resume=resume).delete()
            messages.success(request, "Education removed.")

        elif action == 'delete_experience':
            item_id = request.POST.get('item_id')
            Experience.objects.filter(pk=item_id, resume=resume).delete()
            messages.success(request, "Experience removed.")

        elif action == 'delete_skill':
            item_id = request.POST.get('item_id')
            Skill.objects.filter(pk=item_id, resume=resume).delete()
            messages.success(request, "Skill removed.")

        elif action == 'delete_certification':
            item_id = request.POST.get('item_id')
            Certification.objects.filter(pk=item_id, resume=resume).delete()
            messages.success(request, "Certification removed.")

        return redirect('resume_edit', pk=resume.pk)

    context = {
        'resume': resume,
        'resume_form': resume_form,
        'edu_form': edu_form,
        'exp_form': exp_form,
        'skill_form': skill_form,
        'cert_form': cert_form,
        'score': resume.get_score(),
        'feedback': resume.get_feedback(),
    }
    return render(request, 'core/resume/edit.html', context)


@login_required
def resume_preview(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'core/resume/preview.html', {'resume': resume})


@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, "Resume deleted.")
        return redirect('resume_list')
    return render(request, 'core/resume/delete.html', {'resume': resume})


@login_required
def resume_analyze(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    score = resume.get_score()
    feedback = resume.get_feedback()
    resume.score = score
    resume.save()
    return render(request, 'core/resume/analyze.html', {
        'resume': resume,
        'score': score,
        'feedback': feedback,
    })


# ─── Jobs ─────────────────────────────────────────────────────────────────────

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    job_type = request.GET.get('type', '')
    location = request.GET.get('location', '')

    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(company__icontains=query) |
                           Q(required_skills__icontains=query))
    if category:
        jobs = jobs.filter(category=category)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    # Match percentage if logged in
    resume = None
    if request.user.is_authenticated:
        resume = Resume.objects.filter(user=request.user).first()

    jobs_with_match = []
    for job in jobs:
        pct = job.get_match_percent(resume)
        jobs_with_match.append((job, pct))
    jobs_with_match.sort(key=lambda x: x[1], reverse=True)

    context = {
        'jobs_with_match': jobs_with_match,
        'query': query,
        'category': category,
        'job_type': job_type,
        'location': location,
        'categories': Job.CATEGORY_CHOICES,
        'types': Job.TYPE_CHOICES,
        'total': len(jobs_with_match),
    }
    return render(request, 'core/jobs/list.html', context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    resume = None
    match_pct = 0
    already_applied = False

    if request.user.is_authenticated:
        resume = Resume.objects.filter(user=request.user).first()
        match_pct = job.get_match_percent(resume)
        already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()

    return render(request, 'core/jobs/detail.html', {
        'job': job,
        'match_pct': match_pct,
        'already_applied': already_applied,
        'resume': resume,
    })


@login_required
def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You've already applied to this job.")
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.user, request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            messages.success(request, f"Successfully applied to {job.title} at {job.company}!")
            return redirect('my_applications')
    else:
        form = JobApplicationForm(request.user)

    resume = Resume.objects.filter(user=request.user).first()
    match_pct = job.get_match_percent(resume)
    return render(request, 'core/jobs/apply.html', {'form': form, 'job': job, 'match_pct': match_pct})


@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    return render(request, 'core/jobs/my_applications.html', {'applications': applications})


# ─── Interview Practice ────────────────────────────────────────────────────────

@login_required
def interview_home(request):
    sessions = InterviewSession.objects.filter(user=request.user).order_by('-created_at')
    questions_count = InterviewQuestion.objects.filter(is_active=True).count()
    return render(request, 'core/interview/home.html', {
        'sessions': sessions,
        'questions_count': questions_count,
    })


@login_required
def interview_start(request):
    session = InterviewSession.objects.create(
        user=request.user,
        title=f"Mock Interview #{InterviewSession.objects.filter(user=request.user).count() + 1}"
    )
    return redirect('interview_question', session_id=session.pk)


@login_required
def interview_question(request, session_id):
    session = get_object_or_404(InterviewSession, pk=session_id, user=request.user)
    answered_ids = session.answers.values_list('question_id', flat=True)
    remaining = InterviewQuestion.objects.filter(is_active=True).exclude(id__in=answered_ids)

    if not remaining.exists() or session.answers.count() >= 5:
        session.completed = True
        session.score = session.get_average_score()
        session.save()
        return redirect('interview_results', session_id=session.pk)

    question = remaining.order_by('?').first()

    if request.method == 'POST':
        form = InterviewAnswerForm(request.POST)
        if form.is_valid():
            answer = InterviewAnswer(session=session, question=question,
                                     answer_text=form.cleaned_data['answer'])
            score, feedback = answer.analyze_answer()
            answer.save()
            messages.info(request, f"Answer saved! Score: {score}/100")
            return redirect('interview_question', session_id=session.pk)
    else:
        form = InterviewAnswerForm()

    return render(request, 'core/interview/question.html', {
        'session': session,
        'question': question,
        'form': form,
        'answered_count': session.answers.count(),
        'progress': int((session.answers.count() / 5) * 100),
    })


@login_required
def interview_results(request, session_id):
    session = get_object_or_404(InterviewSession, pk=session_id, user=request.user)
    answers = session.answers.select_related('question').all()
    return render(request, 'core/interview/results.html', {
        'session': session,
        'answers': answers,
        'avg_score': session.get_average_score(),
    })


# ─── Recruiter ────────────────────────────────────────────────────────────────

@login_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    total_apps = JobApplication.objects.filter(job__posted_by=request.user).count()
    return render(request, 'core/recruiter/dashboard.html', {
        'jobs': jobs,
        'total_apps': total_apps,
    })


@login_required
def recruiter_post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, f"Job '{job.title}' posted successfully!")
            return redirect('recruiter_dashboard')
    else:
        form = JobForm()
    return render(request, 'core/recruiter/post_job.html', {'form': form})


@login_required
def recruiter_applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id, posted_by=request.user)
    applications = JobApplication.objects.filter(job=job).select_related('applicant', 'resume')
    return render(request, 'core/recruiter/applicants.html', {
        'job': job,
        'applications': applications,
    })
