from django import forms
from django.contrib.auth.models import User
import models

from . import models

class StudentLoginForm(forms.Form):
    reg_no = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)


class ScoreForm(forms.ModelForm):
    class Meta:
        models = models.CourseItem
        fields = ['student', 'course', 'student_course_ca', 'student_course_exam_score']

