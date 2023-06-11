from rest_framework import serializers

from results.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('profile', 'cgpa')

