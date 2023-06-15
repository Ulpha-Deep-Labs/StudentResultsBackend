from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer


from results.models import CourseItem

User = get_user_model()
