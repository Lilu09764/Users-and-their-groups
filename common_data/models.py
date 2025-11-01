from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='students'
    )

    def __str__(self):
        return self.user.username


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    teacher = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    homework = models.TextField(blank=True)
    room = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.school_class})"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades')
    score = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} — {self.lesson}: {self.score}"


# ---- СИГНАЛЫ ----
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()