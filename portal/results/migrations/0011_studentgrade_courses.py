# Generated by Django 4.2.2 on 2023-06-17 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0010_remove_studentgrade_course_remove_studentgrade_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgrade',
            name='courses',
            field=models.ManyToManyField(to='results.course'),
        ),
    ]