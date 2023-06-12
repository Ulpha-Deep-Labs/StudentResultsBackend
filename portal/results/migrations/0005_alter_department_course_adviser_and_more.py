# Generated by Django 4.2.2 on 2023-06-12 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_alter_department_students_alter_faculty_departments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='course_adviser',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='department',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='students_in_dept', to='results.student'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='departments', to='results.department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(related_name='courses_offered', to='results.course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_dept',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='results.department'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_sch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='results.faculty'),
            preserve_default=False,
        ),
    ]
