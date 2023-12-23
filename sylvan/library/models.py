from django.db import models

# Create your models here.
class LineItem(models.Model):
    id_reservation = models.IntegerField(default=0)
    id_inventory = models.IntegerField(default=0)
    reserved = models.BooleanField(default=False)
    last_updated = models.DateTimeField('auto_now')
    date_created = models.DateTimeField('auto_now_add')

    def __str__(self):
        id = str(self.id_inventory)
        return id

class Reservation(models.Model):
    id_user = models.IntegerField(default=0)

class ReservationStatus(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta():
        verbose_name_plural = 'Reservation Statuses'

class Delinquency(models.Model):
    id_user = models.IntegerField(default=0)
    id_reservation = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)
    last_updated = models.DateTimeField('auto_now')

    def __str__(self):
        return self.id_user
    
    class Meta():
        verbose_name_plural = "Delinquencies"