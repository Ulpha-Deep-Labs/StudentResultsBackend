from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from results.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Include all fields from the model
        depth = 1
