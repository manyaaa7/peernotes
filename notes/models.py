import os
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser


class Branch(models.TextChoices):
    COMMON = 'COMMON', '1st Year Common (All B.Tech Branches)'
    CSE = 'ECS', 'B.Tech. Computer Science & Engineering'
    CSAI = 'EAI', 'B.Tech. Computer Science & Artificial Intelligence'
    EECS = 'EEC', 'B.Tech. Electrical Engineering & Computer Science'
    VLSI = 'EVE', 'B.Tech. Electronics Engineering (VLSI & Embedded Systems)'
    ECE = 'ECE', 'B.Tech. Electronics & Communication Engineering'
    MECH = 'EMA', 'B.Tech. Mechanical & Aerospace Engineering'
    CIVIL = 'ECV', 'B.Tech. Civil, Construction & Sustainability Engineering'
    ROBOTICS = 'ERA', 'B.Tech. Robotics & Automation'
    BIOTECH = 'EBT', 'B.Tech. Biotechnology & Bioengineering'


class Semester(models.IntegerChoices):
    SEM1 = 1, 'Semester 1 (1st Year)'
    SEM2 = 2, 'Semester 2 (1st Year)'
    SEM3 = 3, 'Semester 3 (2nd Year)'
    SEM4 = 4, 'Semester 4 (2nd Year)'
    SEM5 = 5, 'Semester 5 (3rd Year)'
    SEM6 = 6, 'Semester 6 (3rd Year)'
    SEM7 = 7, 'Semester 7 (4th Year)'
    SEM8 = 8, 'Semester 8 (4th Year)'


class StudentUser(AbstractUser):
    email = models.EmailField(unique=True)
    registration_id = models.CharField(max_length=25, blank=True)
    branch = models.CharField(max_length=10, choices=Branch.choices, default=Branch.CSE)
    joining_year = models.PositiveIntegerField(default=2025)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def current_academic_year(self):
        today = date.today()
        year_diff = today.year - self.joining_year + (1 if today.month >= 7 else 0)
        return max(1, min(4, year_diff))

    @property
    def default_semester(self):
        odd_sem = date.today().month >= 7
        yr = self.current_academic_year
        return (yr * 2 - 1) if odd_sem else (yr * 2)

    def __str__(self):
        return f"{self.email} ({self.get_branch_display()})"


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    branch = models.CharField(max_length=10, choices=Branch.choices)
    semester = models.IntegerField(choices=Semester.choices)
    is_elective = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)

    class Meta:
        unique_together = ('code', 'branch', 'semester')
        ordering = ['semester', 'is_elective', 'code']

    def __str__(self):
        return f"{self.code} - {self.title} ({self.branch}, Sem {self.semester})"


class MaterialType(models.TextChoices):
    HANDWRITTEN = 'HANDWRITTEN', 'Handwritten Notes'
    SLIDES = 'SLIDES', 'Lecture Slides / PPT'
    PYQ = 'PYQ', 'Previous Year Question Paper (PYQ)'
    LAB = 'LAB', 'Lab Manual / Code / Record'
    CHEATSHEET = 'CHEATSHEET', 'Cheat Sheet / Formula Sheet'
    OTHER = 'OTHER', 'Other Study Material'


class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, blank=True, help_text="e.g., Unit 1, Unit 2 & 3, All Units")
    material_type = models.CharField(max_length=20, choices=MaterialType.choices, default=MaterialType.HANDWRITTEN)
    tags = models.CharField(max_length=200, blank=True, help_text="Optional comma-separated topics")
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='peernotes_files/%Y/%m/')

    uploaded_by = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='uploaded_notes')
    bookmarked_by = models.ManyToManyField(StudentUser, related_name='bookmarked_notes', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[1].lower()

    @property
    def is_pdf(self):
        return self.file_extension == '.pdf'

    @property
    def is_image(self):
        return self.file_extension in ['.jpg', '.jpeg', '.png', '.webp', '.gif']

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings.exists():
            return 0
        return round(sum(r.score for r in ratings) / ratings.count(), 1)

    def __str__(self):
        return f"[{self.course.code}] {self.title}"


class Rating(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])

    class Meta:
        unique_together = ('note', 'user')
