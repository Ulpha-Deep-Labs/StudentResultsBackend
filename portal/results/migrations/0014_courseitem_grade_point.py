# Generated by Django 4.2.2 on 2023-06-14 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0013_alter_course_lecturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseitem',
            name='grade_point',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
