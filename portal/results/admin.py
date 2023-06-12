from django.contrib import admin
from . import models
from .models import PortalUsers
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class PortalUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_des')




admin.site.register(PortalUsers, PortalUserAdmin)


class CourseItemInline(admin.TabularInline):
    model = models.CourseItem
    raw_id_fields = ['student']

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_code']

    inlines = [CourseItemInline]



admin.site.register(models.Faculty)
admin.site.register(models.Department)
admin.site.register(models.Session)
admin.site.register(models.Student)







