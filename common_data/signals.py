from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=UserProfile)
def assign_user_to_group(sender, instance, **kwargs):
    user = instance.user
    student_group = Group.objects.get(name='Student')
    teacher_group = Group.objects.get(name='Teacher')


    user.groups.remove(student_group, teacher_group)

    if instance.is_student:
        user.groups.add(student_group)
    if instance.is_teacher:
        user.groups.add(teacher_group)