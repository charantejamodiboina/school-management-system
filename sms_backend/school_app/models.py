from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
# Abstract Base User
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='teacher_profile')
    qualifications = models.TextField()
    experience = models.PositiveIntegerField(help_text="Years of experience")

    def __str__(self):
        return self.user.username

# Student Model
class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='student_profile')
    grade = models.CharField(max_length=10)
    attendance_records = models.ManyToManyField(
        'Attendance',
        blank=True,
        related_name='students_attendance'
    )

    def __str__(self):
        return self.user.username

# Attendance Model
class Attendance(models.Model):
    date = models.DateField()
    status_choices = [('Present', 'Present'), ('Absent', 'Absent')]
    status = models.CharField(max_length=10, choices=status_choices)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

# Notice Model
class Notice(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
