from django.db import models

# Create your models here.

class File(models.Model):
    
    date_created = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(null=True)
    file_name = models.CharField(max_length=200, null=True)
    file_extention = models.CharField(max_length=200, null=True)
    deleted = models.BooleanField(null=True, default=False)

class Messages(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=30, null=True)
    message_content = models.CharField(max_length=200, null=True)
    deleted = models.BooleanField(null=True, default=False)
