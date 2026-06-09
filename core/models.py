from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('jobseeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='jobseeker')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.user_type})"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, default='My Resume')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def get_score(self):
        score = 0
        if self.summary and len(self.summary) > 50:
            score += 20
        elif self.summary:
            score += 10
        edu_count = self.educations.count()
        if edu_count >= 2:
            score += 20
        elif edu_count == 1:
            score += 15
        exp_count = self.experiences.count()
        if exp_count >= 2:
            score += 25
        elif exp_count == 1:
            score += 15
        skill_count = self.skills.count()
        if skill_count >= 8:
            score += 25
        elif skill_count >= 4:
            score += 15
        elif skill_count >= 1:
            score += 8
        cert_count = self.certifications.count()
        if cert_count >= 2:
            score += 10
        elif cert_count == 1:
            score += 5
        if self.phone:
            score += 5
        if self.address:
            score += 5
        return min(score, 100)

    def get_feedback(self):
        feedback = []
        if not self.summary or len(self.summary) < 50:
            feedback.append(("warning", "Write a detailed professional summary (at least 50 characters)."))
        if self.educations.count() == 0:
            feedback.append(("danger", "Add your educational background."))
        if self.experiences.count() == 0:
            feedback.append(("warning", "Include work or internship experience."))
        if self.skills.count() < 4:
            feedback.append(("warning", "Add more technical and soft skills (aim for 6+)."))
        if self.certifications.count() == 0:
            feedback.append(("info", "Consider adding certifications to stand out."))
        if not self.phone:
            feedback.append(("info", "Add your contact number."))
        if len(feedback) == 0:
            feedback.append(("success", "Great resume! You're well-prepared for applications."))
        return feedback


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} at {self.school}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')

    def __str__(self):
        return self.name


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    CATEGORY_CHOICES = [
        ('bpo', 'BPO / Call Center'),
        ('it', 'Information Technology'),
        ('remote', 'Remote Work'),
        ('overseas', 'Overseas / OFW'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance & Accounting'),
        ('education', 'Education'),
        ('engineering', 'Engineering'),
    ]
    TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='it')
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='full_time')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    required_skills = models.TextField(help_text="Comma-separated skills")
    salary_min = models.IntegerField(default=0)
    salary_max = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    def get_match_percent(self, resume):
        if not resume:
            return 0
        job_skills = [s.lower() for s in self.get_skills_list()]
        resume_skills = [s.name.lower() for s in resume.skills.all()]
        if not job_skills:
            return 50
        matches = sum(1 for js in job_skills if any(js in rs or rs in js for rs in resume_skills))
        return int((matches / len(job_skills)) * 100)


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Under Review'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"


class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    title = models.CharField(max_length=200, default='Mock Interview Session')
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def get_average_score(self):
        answers = self.answers.all()
        if not answers:
            return 0
        return int(sum(a.score for a in answers) / len(answers))


class InterviewQuestion(models.Model):
    CATEGORY_CHOICES = [
        ('behavioral', 'Behavioral'),
        ('technical', 'Technical'),
        ('situational', 'Situational'),
        ('general', 'General'),
    ]
    question = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    tip = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question[:80]


class InterviewAnswer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    score = models.IntegerField(default=0)
    feedback = models.TextField(blank=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.session.user.username}"

    def analyze_answer(self):
        text = self.answer_text.strip()
        words = len(text.split())
        score = 0
        feedback_parts = []
        if words >= 80:
            score += 40
            feedback_parts.append("Excellent detail in your answer.")
        elif words >= 40:
            score += 30
            feedback_parts.append("Good level of detail.")
        elif words >= 15:
            score += 15
            feedback_parts.append("Consider providing more detail and examples.")
        else:
            score += 5
            feedback_parts.append("Answer is too short. Elaborate more.")
        keywords = ['experience', 'team', 'result', 'achieved', 'improved', 'managed',
                    'developed', 'led', 'created', 'solved', 'challenge', 'learned',
                    'skill', 'project', 'customer', 'growth', 'success']
        matched = sum(1 for kw in keywords if kw in text.lower())
        if matched >= 5:
            score += 35
            feedback_parts.append("Strong use of impactful keywords.")
        elif matched >= 3:
            score += 20
            feedback_parts.append("Good use of relevant keywords.")
        elif matched >= 1:
            score += 10
            feedback_parts.append("Try to include more specific action words.")
        else:
            feedback_parts.append("Use more specific keywords like 'achieved', 'managed', 'improved'.")
        sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        if len(sentences) >= 3:
            score += 25
            feedback_parts.append("Well-structured response.")
        elif len(sentences) >= 2:
            score += 15
        self.score = min(score, 100)
        self.feedback = ' '.join(feedback_parts)
        return self.score, self.feedback


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
