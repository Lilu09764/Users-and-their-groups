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


class StudyGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'is_teacher': True},
        related_name='created_groups'
    )
    students = models.ManyToManyField(
        Student,
        related_name='study_groups',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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
        related_name='lessons',
        null=True,
        blank=True
    )
    study_group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True
    )
    homework = models.TextField(blank=True)
    room = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.school_class:
            return f"{self.subject} ({self.school_class})"
        elif self.study_group:
            return f"{self.subject} [{self.study_group}]"
        return self.subject


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades')
    score = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} — {self.lesson}: {self.score}"

    @property
    def group_context(self):
        if self.lesson.study_group:
            return f"Group: {self.lesson.study_group.name}"
        elif self.lesson.school_class:
            return f"Class: {self.lesson.school_class.name}"
        return "No group"



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()