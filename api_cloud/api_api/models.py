from django.db import models


# Create your models here.
class ApiApi(models.Model):
    name = models.CharField(max_length=100)
    project_id = models.IntegerField(blank=True, null=True)
    api_http_type = models.IntegerField(blank=True, null=True)
    api_url = models.CharField(max_length=500, blank=True, null=True)
    url_list = models.TextField(blank=True, null=True)
    api_domain = models.CharField(max_length=100, blank=True, null=True)
    api_method = models.IntegerField(blank=True, null=True)
    api_headers = models.TextField(blank=True, null=True)
    api_body_type = models.IntegerField(blank=True, null=True)
    api_body_value = models.TextField(blank=True, null=True)
    api_expect_result = models.TextField(blank=True, null=True)
    api_real_result = models.TextField(blank=True, null=True)
    api_is_success = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    creater = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    last_execute_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
