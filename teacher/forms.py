from django import forms
from django.utils import timezone
from common_data.models import Lesson, UserProfile, Student, Grade  # ← добавили Grade


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'date', 'description', 'school_class']

    teacher = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(is_teacher=True),
        empty_label="Select a teacher"
    )

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("The lesson date cannot be in the past!")
        return date



class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'score']

    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        empty_label="Select a student"
    )

    score = forms.IntegerField(
        min_value=1,
        max_value=100,
        label="Grade",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter grade'})
    )

    def __init__(self, *args, **kwargs):
        lesson = kwargs.pop('lesson', None)
        super().__init__(*args, **kwargs)
        if lesson:
            self.fields['student'].queryset = lesson.school_class.students.all()