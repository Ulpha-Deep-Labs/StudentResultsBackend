from rest_framework import generics
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
from .serializers import StudentSerializer, CourseItemSerializer, CourseSerializer, StudentGradeSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)

        except Student.DoesNotExist:
            return Response({'error': 'Student Data not found'}, status=404)







class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        course_items = instance.course_items.all()  # Access the related CourseItem objects
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("Students are not allowed to create courses.")

    def get_permissions(self):
        if self.action == 'create':
            permissions = []  # No permissions for creating courses
        else:
            permissions = [IsAuthenticated]  # Allow authenticated users for other actions

        return [permission() for permission in permissions]


class StudentGradeViewSet(viewsets.ModelViewSet):
    queryset = StudentGrade.objects.all()
    serializer_class = StudentGradeSerializer

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("Students are not allowed to create student grades.")

    def get_permissions(self):
        if self.action == 'create':
            permissions = []  # No permissions for creating student grades
        else:
            permissions = [IsAuthenticated]  # Allow authenticated users for other actions

        return [permission() for permission in permissions]




class CourseItemViewSet(viewsets.ModelViewSet):
    queryset = CourseItem.objects.all()
    serializer_class = CourseItemSerializer

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("Students are not allowed to create course items.")

    def get_permissions(self):
        if self.action == 'create':
            permissions = []  # No permissions for creating course items
        else:
            permissions = [IsAuthenticated]  # Allow authenticated users for other actions

        return [permission() for permission in permissions]