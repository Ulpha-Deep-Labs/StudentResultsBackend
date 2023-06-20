from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()




class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photo/staff/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.username
