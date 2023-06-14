# Generated by Django 4.2.2 on 2023-06-13 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0010_student_courses_offered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses_offered',
        ),
        migrations.AddField(
            model_name='student',
            name='courses_offered',
            field=models.ManyToManyField(related_name='courses_details', to='results.courseitem'),
        ),
    ]