from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from results.models import Student, CourseItem, Course, StudentGrade


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Include all fields from the model
        depth = 1


class CourseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseItem
        fields = '__all__'
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    course_items = CourseItemSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        depth = 1


class StudentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGrade
        fields = '__all__'
        depth = 1