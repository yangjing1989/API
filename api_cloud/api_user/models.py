from django.db import models


class Permission(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
