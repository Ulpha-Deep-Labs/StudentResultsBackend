import django_filters
from results.models import CourseItem, Semester

class CourseItemFilter(django_filters.FilterSet):
    semester_name = django_filters.CharFilter(field_name='course__semester__semester_name')
    session = django_filters.CharFilter(field_name='course__semester__session__session_name')

    class Meta:
        model = CourseItem
        fields = ['semester_name', 'session']