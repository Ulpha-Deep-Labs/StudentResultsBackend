from django.urls import path

from .views import StudentAPIView, UserDetailAPI

urlpatterns = [

    path('', StudentAPIView.as_view(), name = 'student_list'),
    path('users', UserDetailAPI.as_view())

]