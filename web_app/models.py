from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('person', 'Persona'),
        ('quality_manager', 'Quality Manager'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)


class Course(models.Model):
    year = models.IntegerField(null=True, blank=True)
    course_n = models.CharField(max_length=255, null=True, blank=True)
    course_name = models.TextField(null=True, blank=True)
    planned_date = models.DateTimeField(null=True, blank=True)
    effective_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    start = models.CharField(max_length=255, null=True, blank=True)
    check_review = models.CharField(max_length=255, null=True, blank=True)
    end = models.CharField(max_length=255, null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    i_e = models.CharField(max_length=255, null=True, blank=True)
    trainer = models.CharField(max_length=255, null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    requirement = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.course_name}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Pianificato'),
        ('completed', 'Completato'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses_attendances')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users_attendances')
    stato = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.course.id} ({self.stato})"

    class Meta:
        unique_together = ('course', 'user', 'stato')