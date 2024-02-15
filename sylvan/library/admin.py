from django.contrib import admin
from .models import LineItem, Reservation, ReservationStatus, DecisionPoint, Case, ProblemLineItem

# Register your models here.
admin.site.register(LineItem)
admin.site.register(Reservation)
admin.site.register(ReservationStatus)
admin.site.register(DecisionPoint)
admin.site.register(Case)
admin.site.register(ProblemLineItem)