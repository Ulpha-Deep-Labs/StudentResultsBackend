# Generated by Django 4.2.2 on 2023-06-17 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0011_studentgrade_courses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentgrade',
            old_name='courses',
            new_name='courses_offered',
        ),
    ]
