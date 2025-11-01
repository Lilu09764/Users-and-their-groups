from django.db import models
from django.contrib.auth.models import User

class StudentClass(models.Model):
    sclass_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(User, related_name="classes")

    def __str__(self):
        return self.name



