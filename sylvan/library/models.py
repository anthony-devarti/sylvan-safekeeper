from django.db import models
from django.utils import timezone

# Create your models here.
class LineItem(models.Model):
    id_reservation = models.IntegerField(default=0)
    id_inventory = models.IntegerField(default=0)
    #There is an important distinction between hold and lent.
    # Hold means that the item is unavailable to show up in searches
    # lent means that the card is currently not in the lender's posession
    lent = models.BooleanField(default=False)
    hold = models.BooleanField(default=False)
    date_created = models.DateTimeField(editable = False)
    last_updated = models.DateTimeField(editable = False)

    def __str__(self):
        id = str(self.id_inventory)
        return id
    
    def save(self, *args, **kwargs):
        '''on save, update timestamps'''
        if not self.id:
            self.date_created = timezone.now()
        self.last_updated = timezone.now()
        return super(LineItem, self).save(*args, **kwargs)

class ReservationStatus(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta():
        verbose_name_plural = 'Reservation Statuses'

class Reservation(models.Model):
    id_user = models.IntegerField(default=0)
    return_date = models.DateTimeField()
    date_created = models.DateTimeField(editable = False, null=True)
    last_updated = models.DateTimeField(editable = False, null=True)
    stage = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.return_date)
        
class Delinquency(models.Model):
    id_user = models.IntegerField(default=0)
    id_reservation = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)
    last_updated = models.DateTimeField('auto_now')

    def __str__(self):
        return self.id_user
    
    class Meta():
        verbose_name_plural = "Delinquencies"

class DecisionPoint(models.Model):
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    terminal = models.BooleanField(default = False)
    #destination on decline
    #destination on success

    def __str__(self):
        return self.title

