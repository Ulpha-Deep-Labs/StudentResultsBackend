from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from results.models import Student, CourseItem, Course, StudentGrade, Staff, Session, Semester, SemesterGPA

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Include all fields from the model
        depth = 1


class StudentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGrade
        fields = ['total_grade_point', 'total_course_units', 'cgpa', 'courses_offered']


class SemesterGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterGPA
        fields = ['semester', 'gpa', 'total_grade_points', 'total_course_units', 'courses_offered']




class CourseItemSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course.name')
    class Meta:
        model = CourseItem
        fields = ['course', 'student_course_ca', 'student', 'student_course_exam_score', 'total_score', 'grade_point', 'carry_overs']

class StudentCoursesSerializer(serializers.Serializer):
    student_grade = StudentGradeSerializer()
    course_items = CourseItemSerializer(many=True)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'



class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'