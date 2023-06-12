from rest_framework import serializers
from django.contrib.auth import get_user_model
from results.models import Student

from results.models import Student

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('profile','student_dept',
                  'student_sch',
                  'courses','level',
                  'gpa', 'cgpa', 'photo')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]

