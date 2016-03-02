from django.db import models


# Create your models here.
class SimpleItem(models.Model):
    name = models.CharField(max_length=1000)
