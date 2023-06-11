from rest_framework import generics
from results.models import Student
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



from  .serializers import StudentSerializer, UserSerializer


class StudentAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class UserDetailAPI(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
