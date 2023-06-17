from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
User = get_user_model()
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.db.models.signals import m2m_changed


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=200)
    department = models.ManyToManyField('Department', blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

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
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    course_units = models.IntegerField(blank=True)
    lecturer = models.ForeignKey("Staff", on_delete=models.PROTECT)


    def __str__(self):
        return self.course_code



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_reg = models.CharField(max_length=20, unique=True)
    student_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    student_dept = models.ForeignKey('Department', on_delete=models.CASCADE)
    level = models.IntegerField(null=True, blank=True)
    carryovers = models.IntegerField(blank=True, null=True)
    paid_school_fees = models.BooleanField(null=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    photo = models.ImageField(upload_to='photo/student/%Y/%m/%d/', blank=True)





    def __str__(self):
        return self.student_reg

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo/staff/%Y/%m/%d/', blank=True)
    def __str__(self):
        return self.user.username






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
    course = models.ForeignKey(Course, related_name='course_items', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_course_ca = models.IntegerField()
    student_course_exam_score = models.IntegerField()
    student_grade = models.CharField(max_length=1, blank=True, null=True)
    total_score = models.IntegerField(blank=True)
    grade_point = models.IntegerField(blank=True)
    t_grade_point = models.IntegerField(blank=True)
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

        course_grade = self.grade_point * self.course.course_units
        self.t_grade_point = course_grade


        super().save()


    def __str__(self):
        return self.course.course_code


class StudentGrade(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    total_grade_point = models.IntegerField(blank=True, null=True)
    total_course_units = models.IntegerField(blank=True, null=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    courses_offered = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.student.student_reg} "

    def save(self, *args, **kwargs):
        self.total_grade_point = self.calculate_total_grade_point()
        self.total_course_units = self.calculate_total_course_units()
        self.cgpa = self.calculate_gpa()
        super().save(*args, **kwargs)
        self.update_student_cgpa()

    def update_student_cgpa(self):
        self.student.cgpa = self.cgpa
        self.student.save()

    def calculate_total_grade_point(self):
        course_items = CourseItem.objects.filter(student=self.student, course__in=self.courses_offered.all())
        total_grade_point = sum(course_item.t_grade_point for course_item in course_items if course_item.t_grade_point is not None)
        return total_grade_point

    def calculate_total_course_units(self):
        course_items = CourseItem.objects.filter(student=self.student, course__in=self.courses_offered.all())
        total_course_units = sum(course_item.course.course_units for course_item in course_items)
        return total_course_units

    def calculate_gpa(self):
        if self.total_course_units != 0:
            self.gpa = self.total_grade_point / self.total_course_units
        else:
            self.gpa = 0
        return self.gpa

@receiver(post_save, sender=CourseItem)
def update_student_grade(sender, instance, **kwargs):
    student = instance.student
    student_grade, _ = StudentGrade.objects.get_or_create(student=student)
    student_grade.courses_offered.set(student.courseitem_set.values_list('course', flat=True))
    student_grade.save()

@receiver(pre_delete, sender=StudentGrade)
def delete_related_course_items(sender, instance, **kwargs):
    instance.courses_offered.clear()




@receiver(post_save, sender=CourseItem)
def update_student_carryovers(sender, instance, **kwargs):
    # Get the associated Student object
    student = instance.student

    # Count the number of CourseItems with carry_overs=True
    carry_overs_count = CourseItem.objects.filter(student=student, carry_overs=True).count()

    # Update the carryovers field in the Student model
    student.carryovers = carry_overs_count
    student.save()