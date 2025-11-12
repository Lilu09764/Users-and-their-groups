from django import forms
from django.utils import timezone
from common_data.models import Lesson, UserProfile, Student, Grade, SchoolClass, StudyGroup

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'date', 'description', 'school_class', 'study_group', 'homework', 'room']

    teacher = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(is_teacher=True),
        empty_label="Select a teacher"
    )

    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        required=False
    )
    study_group = forms.ModelChoiceField(
        queryset=StudyGroup.objects.all(),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        school_class = cleaned_data.get('school_class')
        study_group = cleaned_data.get('study_group')

        if not school_class and not study_group:
            raise forms.ValidationError("Lesson must belong to either a school class or a study group.")
        if school_class and study_group:
            raise forms.ValidationError("Lesson cannot belong to both a class and a study group at the same time.")

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
            if lesson.school_class:
                self.fields['student'].queryset = lesson.school_class.students.all()
            elif lesson.study_group:
                self.fields['student'].queryset = lesson.study_group.students.all()
            else:
                self.fields['student'].queryset = Student.objects.none()