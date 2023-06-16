from rest_framework import generics
from results.models import  CourseItem, Student
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
from .serializers import StudentSerializer
from rest_framework import status

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


