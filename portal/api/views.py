from rest_framework import generics
from results.models import Student
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserDetailsSerializer




from  .serializers import StudentSerializer, UserSerializer
User = get_user_model()


class StudentAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer