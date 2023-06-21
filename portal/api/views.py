from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from results.models import  CourseItem, Student, Course, StudentGrade, Session, Semester
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
from .serializers import StudentSerializer, CourseItemSerializer, StudentGradeSerializer, StudentCoursesSerializer, CourseSerializer, SemesterSerializer, SessionSerializer
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


class CourseListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        session_name = request.query_params.get('session')
        semester_name = request.query_params.get('semester')

        try:
            session = Session.objects.get(name=session_name)
            semester = Semester.objects.get(session=session, semester_name=semester_name)
        except Session.DoesNotExist:
            return Response({'error': 'Session does not exist'}, status=404)
        except Semester.DoesNotExist:
            return Response({'error': 'Semester does not exist'}, status=404)

        courses = Course.objects.filter(course_items__student=user.student, semester=semester)

        course_data = []
        for course in courses:
            course_items = CourseItem.objects.filter(course=course, student=user.student)
            course_item_data = []
            for course_item in course_items:
                course_item_data.append({
                    'student_course_ca': course_item.student_course_ca,
                    'student_course_exam_score': course_item.student_course_exam_score,
                    'student_grade': course_item.student_grade,
                    'total_score': course_item.total_score,
                    'grade_point': course_item.grade_point,
                    't_grade_point': course_item.t_grade_point,
                    'carry_overs': course_item.carry_overs
                })
            course_data.append({
                'name': course.name,
                'course_code': course.course_code,
                'semester': course.semester.semester_name,
                'course_items': course_item_data
            })

        return Response(course_data)