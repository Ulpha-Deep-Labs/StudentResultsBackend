from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

from .views import StudentAPIView, UserLoginAPIView, UserDetailView

schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [

    path('', StudentAPIView.as_view(), name = 'student_list'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('users/', UserDetailView.as_view(), name='users' ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
    path("schema/main/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui")


]