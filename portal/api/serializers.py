from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from results.models import Student, CourseItem, Course, StudentGrade, Staff, Session, Semester, SemesterGPA, CourseRegistration

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

class CourseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'course_code', 'semester', 'course_units', 'lecturer']

class CourseRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseRegistration
        fields = ['id', 'course', 'student']



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'course_code', 'semester', 'course_units', 'lecturer']

class CourseItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CourseItem
        fields = ['course', 'student_course_ca', 'student_course_exam_score', 'student_grade', 'total_score', 'grade_point', 't_grade_point', 'carry_overs']

class SemesterGPASerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterGPA
        fields = ['semester', 'gpa', 'total_grade_points', 'total_course_units', 'courses_offered']

class StudentGradeSerializer(serializers.ModelSerializer):
    courses_offered = CourseSerializer(many=True)

    class Meta:
        model = StudentGrade
        fields = ['student', 'total_grade_point', 'total_course_units', 'cgpa', 'courses_offered']

class StudentDataSerializer(serializers.Serializer):
    student = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()
    student_grade = serializers.SerializerMethodField()
    course_items = serializers.SerializerMethodField()
    semester_gpa = serializers.SerializerMethodField()

    def get_student(self, obj):
        student = obj['student']
        return {
            'student_reg': student.student_reg,
            'student_faculty': student.student_faculty.name if student.student_faculty else None,
            'student_dept': student.student_dept.name if student.student_dept else None,
            'date_of_birth': student.date_of_birth,
            'level': student.level,
            'carryovers': student.carryovers,
            'paid_school_fees': student.paid_school_fees,
            'cgpa': student.cgpa,
            'photo': student.photo.url if student.photo else None
        }

    def get_semester(self, obj):
        semester = obj['semester']
        return {
            'session': semester.session.name,
            'semester_name': semester.semester_name
        }

    def get_student_grade(self, obj):
        student_grade = obj['student_grade']
        return {
            'total_grade_point': student_grade.total_grade_point,
            'total_course_units': student_grade.total_course_units,
            'cgpa': student_grade.cgpa
        }

    def get_course_items(self, obj):
        course_items = obj['course_items']
        serializer = CourseItemSerializer(course_items, many=True)
        return serializer.data

    def get_semester_gpa(self, obj):
        semester_gpa = obj['semester_gpa']
        return {
            'gpa': semester_gpa.gpa,
            'total_grade_points': semester_gpa.total_grade_points,
            'total_course_units': semester_gpa.total_course_units
        }
