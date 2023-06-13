# Generated by Django 4.2.2 on 2023-06-13 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0007_student_carryovers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='students',
        ),
        migrations.AddField(
            model_name='department',
            name='student',
            field=models.OneToOneField(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='students_in_dept', to='results.student'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='course_adviser',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dept_student', to='results.department'),
        ),
    ]
