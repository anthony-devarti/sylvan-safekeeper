from django.db import models

# Create your models here.
class LineItem(models.Model):
    id_reservation = models.IntegerField(default=0)

class Reservation(models.Model):
    id_user = models.IntegerField(default=0)
    