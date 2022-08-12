from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    GENDER = (
        ('F', 'F'),
        ('M', 'M'),
    )
    userLineId = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "LineMessage",null = True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birth = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    tiredIndex = models.CharField(max_length=100)
    def get_user(self):
        return str(self.user.pk)