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


@api_view(['GET'])
def get_student(request):
    # Your code goes here
    if request.user.is_authenticated:
        user = request.user
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        student = user.student
    except Student.DoesNotExist:
        return Response({'error': 'Student data not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student)
    serialized_data = serializer.data

    return Response(serialized_data, status=status.HTTP_200_OK)





