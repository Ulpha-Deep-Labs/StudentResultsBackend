from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student, Staff

User = get_user_model()

@receiver(post_save, sender=User)
def post_save_create_student(sender, instance, created, **kwargs):
    print("sender", sender)
    print("instance", instance)
    print('created', created)
    if created and instance.role =="student":
        Student.objects.create(user=instance, student_reg=instance.username)
