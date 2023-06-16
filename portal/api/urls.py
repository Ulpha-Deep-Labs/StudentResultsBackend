from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)
from .views import StudentDetailView

schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [
    path("rest-auth/", include("dj_rest_auth.urls")),
    path('student/', StudentDetailView.as_view(), name='get_student'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
    path("schema/main/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui")

]