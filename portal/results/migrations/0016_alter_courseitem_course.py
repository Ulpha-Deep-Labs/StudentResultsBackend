# Generated by Django 4.2.2 on 2023-06-17 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0015_rename_gpa_studentgrade_cgpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseitem',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_items', to='results.course'),
        ),
    ]
