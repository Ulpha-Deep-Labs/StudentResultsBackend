from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)
from .views import StudentDetailView
from rest_framework import routers
from .views import StudentCoursesAPIView, filter_courses_by_lecturer, CourseItemDetailAPIView, CourseListAPIView,CourseRegistrationAPIView


schema_view = get_swagger_view(title='API Documentation')


router = routers.DefaultRouter()

urlpatterns = [
    path("rest-auth/", include("dj_rest_auth.urls")),
    path('student/', StudentDetailView.as_view(), name='get_student'),
    path('courses/', StudentCoursesAPIView.as_view(), name='student_courses'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
    path("schema/main/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('', include(router.urls)),
    path('lecturer-course', filter_courses_by_lecturer, name ='filter_lecturer'),
    path('courses-filter/', CourseListAPIView.as_view(), name='course_item'),
    path('course-registrations/', CourseRegistrationAPIView.as_view(), name='course_reg')
]