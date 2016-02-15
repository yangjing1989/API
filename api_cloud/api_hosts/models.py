from django.db import models


# Create your models here.
class ApiHosts(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    status = models.IntegerField(blank=True)
    is_current = models.BooleanField(blank=True)
    create_time = models.DateTimeField(blank=True)
