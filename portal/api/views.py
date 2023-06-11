from rest_framework import generics
from results.models import Student

from  .serializers import StudentSerializer


class StudentAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Create your views here.
