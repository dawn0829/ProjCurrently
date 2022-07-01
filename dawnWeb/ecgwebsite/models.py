from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def upload_to(instance, filename):
    return f'ECGRecord/{instance.user.username}/{filename}'
    
class ECGRecord(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "ECGRecoed",null = True)
    ecgrecord = models.FileField(upload_to = upload_to)
    detecttime = models.DateTimeField(auto_now = True) 
    def get_user(self):
        return str(self.user.pk)