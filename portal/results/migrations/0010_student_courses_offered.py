# Generated by Django 4.2.2 on 2023-06-13 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_remove_department_course_adviser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='courses_offered',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses_details', to='results.courseitem'),
        ),
    ]
