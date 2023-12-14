from django.contrib import admin
from .models import LineItem, Reservation, ReservationStatus

# Register your models here.
admin.site.register(LineItem)
admin.site.register(Reservation)
admin.site.register(ReservationStatus)