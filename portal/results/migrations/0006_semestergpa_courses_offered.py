# Generated by Django 4.2.2 on 2023-06-22 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_semestergpa_total_course_units_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='semestergpa',
            name='courses_offered',
            field=models.ManyToManyField(to='results.course'),
        ),
    ]
