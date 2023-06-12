from rest_framework import generics
from results.models import Student
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication



from  .serializers import StudentSerializer, UserSerializer
User = get_user_model()


class StudentAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class UserDetailView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # Authentication Successful
            return Response({'message': 'Login Successful'})
        else:
            #Authentication Failed
            return Response({'message': 'Invalid Credentials'}, status =401)
