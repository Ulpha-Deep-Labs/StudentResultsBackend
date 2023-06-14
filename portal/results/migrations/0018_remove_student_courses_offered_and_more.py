# Generated by Django 4.2.2 on 2023-06-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0017_course_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses_offered',
        ),
        migrations.AddField(
            model_name='courseitem',
            name='carry_overs',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
