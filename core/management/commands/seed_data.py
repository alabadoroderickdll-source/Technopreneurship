"""
Management command: python manage.py seed_data
Seeds the database with sample users, jobs, resumes, and interview questions.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (UserProfile, Resume, Education, Experience, Skill,
                         Certification, Job, InterviewQuestion)


class Command(BaseCommand):
    help = 'Seed CareerSync with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('🌱 Seeding CareerSync sample data...'))

        # ── Interview Questions ────────────────────────────────────────────────
        questions = [
            ("Tell me about yourself.", "general",
             "Use the Present-Past-Future structure: current role, how you got here, and where you want to go."),
            ("Why should we hire you?", "general",
             "Focus on 2–3 unique strengths that directly match the job requirements."),
            ("What are your greatest strengths?", "behavioral",
             "Choose strengths that are relevant to the job and back each with a brief example."),
            ("What is your greatest weakness?", "behavioral",
             "Mention a real weakness but show how you are actively working to improve it."),
            ("Describe a challenge you faced and how you handled it.", "situational",
             "Use the STAR method: Situation, Task, Action, Result."),
            ("Where do you see yourself in 5 years?", "general",
             "Align your goals with the company's growth and show ambition."),
            ("Why do you want to work here?", "general",
             "Research the company beforehand. Mention specific things that attract you."),
            ("Describe a time you worked in a team.", "behavioral",
             "Highlight collaboration, communication, and your specific contribution."),
            ("How do you handle stress and pressure?", "behavioral",
             "Provide a concrete example and the techniques you use to stay productive."),
            ("Do you have any questions for us?", "general",
             "Always prepare 2–3 thoughtful questions about the role, team, or company."),
        ]
        created_q = 0
        for q_text, cat, tip in questions:
            obj, created = InterviewQuestion.objects.get_or_create(
                question=q_text,
                defaults={'category': cat, 'tip': tip, 'is_active': True}
            )
            if created:
                created_q += 1
        self.stdout.write(f'  ✅ {created_q} interview questions created')

        # ── Jobs ───────────────────────────────────────────────────────────────
        jobs_data = [
            {
                'title': 'Customer Service Representative',
                'company': 'Teleperformance Philippines',
                'location': 'Eastwood, Quezon City',
                'category': 'bpo',
                'job_type': 'full_time',
                'description': 'Handle inbound and outbound calls for a US-based insurance client. Provide excellent customer support and resolve inquiries efficiently.',
                'requirements': 'At least 6 months BPO experience\nExcellent English communication skills\nWilling to work on shifting schedules\nComputer literate',
                'required_skills': 'Customer Service, Communication, Problem Solving, Microsoft Office, English',
                'salary_min': 18000,
                'salary_max': 25000,
            },
            {
                'title': 'Junior Django Developer',
                'company': 'Accenture Philippines',
                'location': 'BGC, Taguig City',
                'category': 'it',
                'job_type': 'full_time',
                'description': 'Join our growing engineering team to build scalable web applications using Django and modern cloud infrastructure.',
                'requirements': 'Bachelor\'s degree in Computer Science or related field\nProficiency in Python and Django\nKnowledge of RESTful APIs\nFamiliarity with Git',
                'required_skills': 'Python, Django, SQL, REST API, Git, HTML/CSS, JavaScript',
                'salary_min': 35000,
                'salary_max': 55000,
            },
            {
                'title': 'Remote Virtual Assistant',
                'company': 'MyOutDesk',
                'location': 'Remote (Philippines)',
                'category': 'remote',
                'job_type': 'full_time',
                'description': 'Provide administrative and operational support to US-based real estate professionals. Work from home with flexible hours.',
                'requirements': 'Strong organizational skills\nExcellent written and verbal English\nExperience with CRM tools preferred\nReliable internet connection (at least 25 Mbps)',
                'required_skills': 'Communication, Microsoft Office, Time Management, CRM, Data Entry, Organization',
                'salary_min': 28000,
                'salary_max': 40000,
            },
            {
                'title': 'Registered Nurse (Saudi Arabia)',
                'company': 'King Faisal Hospital',
                'location': 'Riyadh, Saudi Arabia',
                'category': 'overseas',
                'job_type': 'contract',
                'description': 'Provide professional nursing care to patients in a world-class hospital in Saudi Arabia. 2-year contract with housing and flight allowance.',
                'requirements': 'Active PRC nursing license\nMinimum 2 years clinical experience\nDataflow verification required\nPASS NCLEX or HAAD preferred',
                'required_skills': 'Patient Care, Clinical Skills, BLS/ACLS, Communication, Medical Documentation',
                'salary_min': 80000,
                'salary_max': 120000,
            },
            {
                'title': 'Technical Support Specialist',
                'company': 'Concentrix',
                'location': 'Ortigas Center, Pasig City',
                'category': 'bpo',
                'job_type': 'full_time',
                'description': 'Provide Tier 1 and Tier 2 technical support for a leading US software company. Troubleshoot software and hardware issues via phone and chat.',
                'requirements': 'IT-related course graduate\nAt least 1 year technical support experience\nKnowledge of Windows OS and networking basics\nWilling to work night shifts',
                'required_skills': 'Technical Support, Windows, Networking, Troubleshooting, Customer Service, Communication',
                'salary_min': 22000,
                'salary_max': 32000,
            },
            {
                'title': 'Full Stack Developer (React + Node)',
                'company': 'Sprout Solutions',
                'location': 'Makati City (Hybrid)',
                'category': 'it',
                'job_type': 'full_time',
                'description': 'Build and maintain our HR SaaS platform used by 1000+ Philippine companies. Work in an agile team with modern tech stack.',
                'requirements': '3+ years experience in full-stack development\nStrong proficiency in React.js and Node.js\nExperience with PostgreSQL or MySQL\nAble to work independently',
                'required_skills': 'React, Node.js, JavaScript, TypeScript, PostgreSQL, REST API, Git, AWS',
                'salary_min': 60000,
                'salary_max': 90000,
            },
            {
                'title': 'Freelance Graphic Designer',
                'company': '99designs',
                'location': 'Remote (Worldwide)',
                'category': 'remote',
                'job_type': 'freelance',
                'description': 'Join our global freelance marketplace. Create logos, social media graphics, and brand identities for international clients.',
                'requirements': 'Strong portfolio of design work\nProficiency in Adobe Creative Suite\nAble to meet client deadlines\nGood English communication',
                'required_skills': 'Photoshop, Illustrator, InDesign, Canva, Typography, Branding, Communication',
                'salary_min': 30000,
                'salary_max': 80000,
            },
            {
                'title': 'Seaman / Able Seaman',
                'company': 'Philippine Transmarine Carriers',
                'location': 'International Waters',
                'category': 'overseas',
                'job_type': 'contract',
                'description': 'Join our international fleet as an Able Seaman. 9-month contract with competitive salary and benefits package.',
                'requirements': 'Valid STCW certificates\nSIRB required\nPhysically fit with valid PEME\nAt least 2 years experience onboard',
                'required_skills': 'Seamanship, Navigation, Safety Procedures, Physical Fitness, Teamwork',
                'salary_min': 70000,
                'salary_max': 100000,
            },
            {
                'title': 'Data Entry Specialist',
                'company': 'TaskUs Philippines',
                'location': 'Santa Rosa, Laguna',
                'category': 'bpo',
                'job_type': 'full_time',
                'description': 'Process and manage data for our global clients with high accuracy. Entry-level position with growth opportunities.',
                'requirements': 'At least senior high school graduate\nTyping speed of 50 WPM\nStrong attention to detail\nComputer literate',
                'required_skills': 'Data Entry, Microsoft Excel, Typing, Attention to Detail, Organization',
                'salary_min': 15000,
                'salary_max': 18000,
            },
            {
                'title': 'Software QA Engineer',
                'company': 'Exist Software Labs',
                'location': 'Eastwood, Quezon City',
                'category': 'it',
                'job_type': 'full_time',
                'description': 'Test and ensure quality of web and mobile applications for enterprise clients across Asia and the US.',
                'requirements': 'BS Computer Science or IT\nExperience with manual and automated testing\nKnowledge of Selenium or Cypress preferred\nStrong analytical skills',
                'required_skills': 'Software Testing, Selenium, JIRA, SQL, Python, Test Cases, Communication',
                'salary_min': 30000,
                'salary_max': 50000,
            },
        ]

        created_jobs = 0
        for j in jobs_data:
            obj, created = Job.objects.get_or_create(
                title=j['title'], company=j['company'],
                defaults=j
            )
            if created:
                created_jobs += 1
        self.stdout.write(f'  ✅ {created_jobs} jobs created')

        # ── Users & Profiles ───────────────────────────────────────────────────
        users_data = [
            ('demo_user', 'Demo', 'User', 'demo@careersync.ph', 'jobseeker'),
            ('maria_reyes', 'Maria', 'Reyes', 'maria@careersync.ph', 'jobseeker'),
            ('jose_mendoza', 'Jose', 'Mendoza', 'jose@careersync.ph', 'jobseeker'),
            ('ana_cruz', 'Ana', 'Cruz', 'ana@careersync.ph', 'jobseeker'),
            ('recruiter_mark', 'Mark', 'Santos', 'mark@techcorp.ph', 'recruiter'),
        ]

        created_users = 0
        for username, first, last, email, utype in users_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='CareerSync2024!',
                    first_name=first,
                    last_name=last,
                    email=email
                )
                UserProfile.objects.create(user=user, user_type=utype)
                created_users += 1
        self.stdout.write(f'  ✅ {created_users} users created')

        # ── Sample Resume for demo_user ────────────────────────────────────────
        try:
            demo = User.objects.get(username='demo_user')
            if not Resume.objects.filter(user=demo).exists():
                resume = Resume.objects.create(
                    user=demo,
                    title='Software Developer Resume',
                    full_name='Demo User',
                    email='demo@careersync.ph',
                    phone='+63 912 345 6789',
                    address='Quezon City, Metro Manila',
                    summary='Motivated software developer with 2 years of experience building web applications using Python and Django. Passionate about clean code, continuous learning, and delivering great user experiences. Seeking remote or hybrid opportunities in Manila or abroad.'
                )
                Education.objects.create(resume=resume, school='University of the Philippines Diliman', degree='Bachelor of Science', field_of_study='Computer Science', start_year='2018', end_year='2022')
                Experience.objects.create(resume=resume, job_title='Junior Web Developer', company='Freelance / Upwork', location='Remote', start_date='Jan 2022', end_date='', is_current=True, description='Developed custom Django web applications for clients in the US and Australia. Handled full-stack development including database design, API development, and front-end implementation.')
                Experience.objects.create(resume=resume, job_title='IT Intern', company='Globe Telecom', location='BGC, Taguig', start_date='Jun 2021', end_date='Dec 2021', is_current=False, description='Assisted the IT team in maintaining internal systems and building automation scripts in Python.')
                for skill_name, level in [('Python', 'advanced'), ('Django', 'advanced'), ('JavaScript', 'intermediate'), ('SQL', 'intermediate'), ('Git', 'intermediate'), ('HTML/CSS', 'advanced'), ('REST API', 'intermediate'), ('Communication', 'advanced')]:
                    Skill.objects.create(resume=resume, name=skill_name, level=level)
                Certification.objects.create(resume=resume, name='Python for Everybody', issuer='Coursera / University of Michigan', year='2021')
                Certification.objects.create(resume=resume, name='AWS Cloud Practitioner', issuer='Amazon Web Services', year='2023')
                self.stdout.write('  ✅ Sample resume created for demo_user')
        except User.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS('\n🎉 Seeding complete! You can now log in with:'))
        self.stdout.write('   Username: demo_user')
        self.stdout.write('   Password: CareerSync2024!')
        self.stdout.write('\n   Admin: python manage.py createsuperuser')
