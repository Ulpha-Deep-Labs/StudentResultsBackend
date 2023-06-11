from rest_framework import serializers
from django.contrib.auth.models import User

from results.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('profile', 'cgpa')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]
