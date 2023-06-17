from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from results.models import Student, CourseItem, Course, StudentGrade


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Include all fields from the model
        depth = 1


class StudentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGrade
        fields = ['total_grade_point', 'total_course_units', 'cgpa', 'courses_offered']

class CourseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseItem
        fields = ['course', 'student_course_ca', 'student_course_exam_score', 'total_score', 'grade_point', 'carry_overs']
        depth = 2

class StudentCoursesSerializer(serializers.Serializer):
    student_grade = StudentGradeSerializer()
    course_items = CourseItemSerializer(many=True)