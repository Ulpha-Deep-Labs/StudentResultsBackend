# Generated by Django 4.2.2 on 2023-06-11 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_remove_student_student_dept_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_dept',
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_sch',
        ),
        migrations.AddField(
            model_name='student',
            name='student_dept',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='results.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='student_sch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='results.faculty'),
            preserve_default=False,
        ),
    ]
