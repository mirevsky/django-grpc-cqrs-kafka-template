from django.db import models


# Create your models here.
class PersonModel(models.Model):
    query = models.CharField(max_length=60)
    page_number = models.IntegerField()
    result_per_page = models.IntegerField()
