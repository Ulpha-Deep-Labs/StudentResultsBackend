from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from results.models import  CourseItem, Student, Course, StudentGrade, Session, Semester, SemesterGPA, CourseRegistration
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import StudentSerializer, CourseItemSerializer, StudentGradeSerializer, StudentCoursesSerializer, CourseSerializer, SemesterSerializer, SessionSerializer, SemesterGradeSerializer, CourseRegistrationSerializer,  CourseSerializer2
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

class StudentDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)

        except Student.DoesNotExist:
            return Response({'error': 'Student Data not found'}, status=404)






class StudentCoursesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        student = request.user.student  # Assuming the authenticated user is a student
        student_grade = student.studentgrade
        course_items = CourseItem.objects.filter(student=student)
        serializer = StudentCoursesSerializer({
            'student_grade': student_grade,
            'course_items': course_items
        })
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication for the view
def filter_courses_by_lecturer(request):
    lecturer = request.user.staff  # Retrieve the authenticated lecturer
    courses = Course.objects.filter(lecturer=lecturer)
    serialized_courses = CourseSerializer(courses, many=True)
    return Response(serialized_courses.data)


class CourseItemDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CourseItem.objects.all()
    serializer_class = CourseItemSerializer


class CourseListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        session_name = self.request.query_params.get('session')
        semester_name = self.request.query_params.get('semester')

        session = get_object_or_404(Session, name=session_name)
        semester = get_object_or_404(Semester, session=session, semester_name=semester_name)

        queryset = Course.objects.filter(course_items__student=user.student, semester=semester)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Retrieve the StudentGrade instance for the logged-in user
        User = get_user_model()
        student = User.objects.get(username=request.user.username).student
        student_grade = get_object_or_404(StudentGrade, student=student)

        # Serialize the StudentGrade data separately using the StudentGradeSerializer
        student_grade_serializer = StudentGradeSerializer(student_grade)

        # Retrieve the SemesterGPA instance for the specific semester and StudentGrade
        session_name = self.request.query_params.get('session')
        semester_name = self.request.query_params.get('semester')
        semester = get_object_or_404(Semester, session__name=session_name, semester_name=semester_name)
        semester_gpa = get_object_or_404(SemesterGPA, student_grade=student_grade, semester=semester)

        # Serialize the SemesterGPA data using the SemesterGPASerializer
        semester_gpa_serializer = SemesterGradeSerializer(semester_gpa)

        # Merge the serialized StudentGrade and SemesterGPA data into the API response
        data = {
            'courses': serializer.data,
            'student_grade': student_grade_serializer.data,
            'semester_gpa': semester_gpa_serializer.data
        }

        return Response(data)


class CourseRegistrationAPIView(generics.ListCreateAPIView):
    serializer_class = CourseRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student = self.request.user.student
        registered_course_ids = CourseRegistration.objects.filter(student=student).values_list('course', flat=True)
        available_courses = Course.objects.exclude(id__in=registered_course_ids)
        return available_courses

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        student = self.request.user.student
        course = serializer.validated_data.get('course')
        if CourseRegistration.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError('The course has already been registered.')
        serializer.save(student=student)
        return Response({'message': 'Course registration successful.'}, status=201)