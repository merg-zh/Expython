from django.db import models
from django_mysql.models import ListCharField

class data(models.Model):
    username = models.CharField(max_length=20)
    list_data = models.CharField(max_length=400, default='')
    type_data = models.CharField(max_length=400,default='')
    title = ListCharField(
        base_field=models.CharField(max_length=20),
        size=200,
        max_length=(200 * 21),
    )
    text_data = ListCharField(
        base_field=models.CharField(max_length=20000),
        size=200,
        max_length=(200 * 20001),
    )
    id_data = ListCharField(
        base_field = models.CharField(max_length=5),
        size=200,
        max_length=(200 * 6)
    )
    post_data = ListCharField(
        base_field = models.CharField(max_length=10),
        size=200,
        max_length=(200 * 11)
    )

class post_data(models.Model):
    username = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    text_data = models.CharField(max_length=20000)
    id_data = models.CharField(max_length=5)
    type_data = models.CharField(max_length=1, default='')

