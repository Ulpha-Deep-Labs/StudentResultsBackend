from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
User = get_user_model()


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=200)
    departments = models.ManyToManyField('Department', related_name='departments',blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name





class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_reg = models.CharField(max_length=20, unique=True)
    student_dept = models.ForeignKey('Department', on_delete=models.CASCADE)
    level = models.IntegerField(null=True, blank=True)
    carryovers = models.IntegerField(blank=True, null=True)
    paid_school_fees = models.BooleanField(null=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    photo = models.ImageField(upload_to='photo/student/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.student_reg

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo/staff/%Y/%m/%d/', blank=True)
    def __str__(self):
        return self.user.username



class Session(models.Model):
    SESSION_CHOICES = [
        ('first', 'First'),
        ('second', 'Second'),
    ]
    year= models.PositiveIntegerField()
    semester = models.CharField(max_length=10, choices=SESSION_CHOICES)

    def __str__(self):
        return f'{str(self.year)} - {self.semester} '





class Course(models.Model):
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    units = models.IntegerField(blank=True)
    lecturer = models.ForeignKey(Staff, on_delete=models.PROTECT)


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
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    student_course_ca = models.IntegerField()
    student_course_exam_score = models.IntegerField()
    student_grade = models.CharField(max_length=1, blank=True, null=True)
    total_score = models.IntegerField(blank=True)
    grade_point = models.IntegerField(blank=True)
    carry_overs = models.BooleanField()


    def save(self):
        score = self.student_course_ca + self.student_course_exam_score
        self.total_score = score
        grade_mapping = {
            (70, 100): "A",
            (60, 69): "B",
            (50, 59): "C",
            (45, 49): "D",
            (40, 44): "E"
        }

        for score_range, grade in grade_mapping.items():
            if score_range[0] <= score <= score_range[1]:
                self.student_grade = grade
                break
        else:
            self.student_grade = "F"

        if self.student_grade =='A':
            self.grade_point =5
        elif self.student_grade =='B':
            self.grade_point =4
        elif self.student_grade =='C':
            self.grade_point =3
        elif self.student_grade =='D':
            self.grade_point =2
        elif self.student_grade =='E':
            self.grade_point =1

        elif self.student_grade =='F':
            self.grade_point =0

        if self.student_grade =='F':
            self.carry_overs = True
        super().save()



    def get_total(self):
        for self.course in self.student.username:
            return len(self.course.course_code)


    def __str__(self):
        return self.course.course_code
