# Generated by Django 4.2.2 on 2023-06-16 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_courseitem_t_grade_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgrade',
            name='gpa',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]