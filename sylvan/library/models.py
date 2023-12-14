from django.db import models

# Create your models here.
class LineItem(models.Model):
    id_reservation = models.IntegerField(default=0)

class Reservation(models.Model):
    id_user = models.IntegerField(default=0)

class ReservationStatus(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta():
        verbose_name_plural = 'Reservation Statuses'