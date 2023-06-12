from django.urls import path

from .views import StudentAPIView, UserLoginAPIView

urlpatterns = [

    path('', StudentAPIView.as_view(), name = 'student_list'),
    path('login/', UserLoginAPIView.as_view(), name='user_login')

]