from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=200)
    departments = models.ManyToManyField('Department', related_name='departments',blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)
    course_adviser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    students = models.ManyToManyField('Student', related_name='students_in_dept', blank=True)

    LEVEL= (
        ("1", "100"),
        ("2", "200"),
        ("3", "300"),
        ("4", "400"),
        ("5", "500"),
        ("6", "600"),
        ("7", "700"),
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL,
        default='1'
    )

    def __str__(self):
        return self.name





class PortalUsers(AbstractUser):
    user_des = models.CharField(max_length=200)
    username = models.CharField(max_length=150, unique=True,
                                validators=[RegexValidator(
                                    regex='^[0-9]+$',
                                    message='Username must be your Reg Number Only',
                                    code='invalid_username')])

    def clean(self):
        super().clean()

        if self.is_superuser:
            return

        if not self.username.isdigit():
            raise ValidationError({'username': 'username must contain omly numbers'})

    def __str__(self):
        return f' {self.username} - {self.email}'


class Student(models.Model):
    profile = models.OneToOneField('PortalUsers', on_delete=models.CASCADE)
    student_dept = models.ForeignKey('Department', on_delete=models.CASCADE )
    student_sch = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', related_name='courses_offered')
    level = models.CharField(max_length=3)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f' {self.profile.username} - {self.profile.first_name}'

class Session(models.Model):
    session_year = models.CharField(max_length=50)
    semester = models.CharField(max_length=20)

    def __str__(self):
        return self.session_year





class Course(models.Model):
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20)
    lecturer = models.OneToOneField(PortalUsers, on_delete=models.PROTECT)

    def __str__(self):
        return self.course_code
    #student_offering_course = models.ForeignKey(Student, related_name='students_offering_course', on_delete=models.CASCADE)
    #student_course_ca = models.IntegerField()
    #student_course_exam_score = models.IntegerField()
    #student_grade = models.CharField(max_length=1, blank=True)

"""
    def save(self, *args, **kwargs):
        if self.student_course_ca + self.student_course_exam_score >=70:
            self.student_grade = "A"
        elif self.student_course_ca + self.student_course_exam_score >=69:
            self.student_grade = "B"
        elif self.student_course_ca + self.student_course_exam_score >=59:
            self.student_grade ="C"

        else:
            self.grade = "D"
        super().save(*args, **kwargs) """


class CourseItem(models.Model):
    course = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    student_course_ca = models.IntegerField(null=True)
    student_course_exam_score = models.IntegerField(null=True)
    student_grade = models.CharField(max_length=1, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.student_course_ca + self.student_course_exam_score >=70:
            self.student_grade = "A"
        elif self.student_course_ca + self.student_course_exam_score >=69:
            self.student_grade = "B"
        elif self.student_course_ca + self.student_course_exam_score >=59:
            self.student_grade ="C"

        else:
            self.grade = "D"
        super().save(*args, **kwargs)

    def get_total(self):
        for self.course in self.student.username:
            return len(self.course.course_code)
