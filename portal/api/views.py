from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from results.models import  CourseItem, Student, Course, StudentGrade
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import StudentSerializer, CourseItemSerializer, StudentGradeSerializer, StudentCoursesSerializer, CourseSerializer
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
