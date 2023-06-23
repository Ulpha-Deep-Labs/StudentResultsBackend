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
from staff.models import Staff


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{str(self.name)} '


class Semester(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    semester_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{str(self.semester_name)} - {self.session.name}'


class Course(models.Model):
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course_units = models.IntegerField(blank=True)
    lecturer = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_code


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_reg = models.CharField(max_length=20, unique=True)
    student_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    student_dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    carryovers = models.IntegerField(blank=True, null=True)
    paid_school_fees = models.BooleanField(null=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    photo = models.ImageField(upload_to='photo/student/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.student_reg

    # student_offering_course = models.ForeignKey(Student, related_name='students_offering_course', on_delete=models.CASCADE)
    # student_course_ca = models.IntegerField()
    # student_course_exam_score = models.IntegerField()
    # student_grade = models.CharField(max_length=1, blank=True)


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

    def update_student_carryovers(self):
        # Get the associated Student object
        student = self.student

        # Calculate the total carry over value
        carry_overs_total = CourseItem.objects.filter(student=student, carry_overs=True).aggregate(total_carry_overs=Sum('carry_overs'))

        # Retrieve the total carry over value or set it to 0 if it's None
        total_carry_overs = carry_overs_total['total_carry_overs'] or 0

        # Update the carryovers field in the Student model
        student.carryovers = total_carry_overs
        student.save()

    def save(self, *args, **kwargs):
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

        if self.student_grade == 'A':
            self.grade_point = 5
        elif self.student_grade == 'B':
            self.grade_point = 4
        elif self.student_grade == 'C':
            self.grade_point = 3
        elif self.student_grade == 'D':
            self.grade_point = 2
        elif self.student_grade == 'E':
            self.grade_point = 1

        elif self.student_grade == 'F':
            self.grade_point = 0

        if self.student_grade == 'F':
            self.carry_overs = True
        else:
            self.carry_overs = False

        course_grade = self.grade_point * self.course.course_units
        self.t_grade_point = course_grade

        self.update_student_carryovers()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.course.course_code


class SemesterGPA(models.Model):
    student_grade = models.ForeignKey("StudentGrade", on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_grade_points = models.IntegerField(blank=True, null=True)
    total_course_units = models.IntegerField(blank=True, null=True)
    courses_offered = models.ManyToManyField(Course)



    def __str__(self):
        return f" {self.student_grade.student.student_reg} - {self.semester}   "

    def save(self, *args, **kwargs):
        self.courses_offered.set(self.student_grade.courses_offered.filter(semester=self.semester))
        super().save(*args, **kwargs)



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
        self.update_student_cgpa()
        super().save(*args, **kwargs)
        self.student.save()
        self.update_semester_gpas()


    def update_student_cgpa(self):
        self.student.cgpa = self.cgpa
        self.student.save()

    def calculate_total_grade_point(self):
        course_items = CourseItem.objects.filter(student=self.student, course__in=self.courses_offered.all())
        total_grade_point = sum(
            course_item.t_grade_point for course_item in course_items if course_item.t_grade_point is not None)
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

    def update_semester_gpas(self):
        semesters = Semester.objects.all()
        for semester in semesters:
            semester_gpa, created = SemesterGPA.objects.get_or_create(student_grade=self, semester=semester)
            semester_gpa.total_grade_points = self.calculate_total_grade_point_by_semester(semester)
            semester_gpa.total_course_units = self.calculate_total_course_units_by_semester(semester)
            semester_gpa.gpa = self.calculate_gpa_by_semester(semester)
            semester_gpa.save()

    def calculate_total_grade_point_by_semester(self, semester):
        course_items = CourseItem.objects.filter(student=self.student, course__semester=semester)
        total_grade_point = sum(
            course_item.t_grade_point for course_item in course_items if course_item.t_grade_point is not None)
        return total_grade_point

    def calculate_total_course_units_by_semester(self, semester):
        course_items = CourseItem.objects.filter(student=self.student, course__semester=semester)
        total_course_units = sum(course_item.course.course_units for course_item in course_items)
        return total_course_units

    def calculate_gpa_by_semester(self, semester):
        total_grade_point = self.calculate_total_grade_point_by_semester(semester)
        total_course_units = self.calculate_total_course_units_by_semester(semester)
        if total_course_units != 0:
            gpa = total_grade_point / total_course_units
        else:
            gpa = 0
        return gpa


@receiver(post_save, sender=CourseItem)
def update_student_grade(sender, instance, **kwargs):
    student = instance.student
    student_grade, _ = StudentGrade.objects.get_or_create(student=student)
    student_grade.courses_offered.set(student.courseitem_set.values_list('course', flat=True))
    student_grade.save()
    student_grade.update_semester_gpas()





class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Create a CourseItem entry for the registered course
        course_item = CourseItem.objects.create(
            course=self.course,
            student=self.student,
            student_course_ca=0,
            student_course_exam_score=0,
            student_grade='',
            total_score=0,
            grade_point=0,
            t_grade_point=0,
            carry_overs=False
        )
        super(CourseRegistration, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the associated CourseItem entry
        course_item = CourseItem.objects.get(course=self.course, student=self.student)
        course_item.delete()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f'{self.student.student_reg} Registered {self.course}  '



