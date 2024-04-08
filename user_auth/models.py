from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=12, null=True, blank=True)


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=100)
    file_size = models.IntegerField()

    def __str__(self):
        return str(self.pk)