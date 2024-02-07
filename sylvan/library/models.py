from django.db import models
from django.utils import timezone

# Create your models here.

class ReservationStatus(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    responsibility = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta():
        verbose_name_plural = 'Reservation Statuses'

class DecisionPoint(models.Model):
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    #a terminal decision point means that the decision can end the reservation process based on the response.
    terminal = models.BooleanField(default = False)
    #check these, because I got them mixed up at one point.
    destination_on_decline = models.ForeignKey(ReservationStatus, related_name='destination_on_decline', on_delete=models.CASCADE)
    destination_on_success = models.ForeignKey(ReservationStatus, related_name='destination_on_success', on_delete=models.CASCADE)
    accept_button = models.CharField(max_length = 200, default ='Accept')
    decline_button = models.CharField(max_length = 200, default='Decline') 
    responsibility = models.CharField(max_length=200, default='borrower')
    header = models.CharField(max_length=200, default='Decision')
    button_text = models.CharField(max_length=200, default='Address Action')


    def __str__(self):
        return self.title

class Reservation(models.Model):
    id_user = models.IntegerField(default=0)
    return_date = models.DateTimeField()
    date_created = models.DateTimeField(editable = False, null=True)
    last_updated = models.DateTimeField(editable = False, null=True)
    stage = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE, default=13, null=True)
    complete = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)
    default_state = models.BooleanField(default=False)
    action_required = models.ForeignKey(DecisionPoint, on_delete=models.CASCADE)

    def submit(self):
        from .serializers import LineItemSerializer
        unrequested_status = ReservationStatus.objects.get(name='Unrequested')

        # check to ensure the reservation being submitted is unrequested
        if self.stage == unrequested_status:
            # Additional logic for submitting reservation if needed...
            
            # Perform actions when reservation is submitted
            lineitems = self.lineitem.all()
            lineitem_serializer = LineItemSerializer(lineitems, many=True)
            serialized_lineitems = lineitem_serializer.data
            
            # Transition to the next appropriate status, e.g., "Pending"
            # Replace the following line with the appropriate status transition
            try:
                self.stage = ReservationStatus.objects.get(name='Pending')
            except ReservationStatus.DoesNotExist as e:
                print(f"Error: {e}")
            self.save()

            return {"message": "Reservation submitted successfully.", "status": self.stage.name, "lineitems": serialized_lineitems}

        return {"message": "Cannot submit reservation. Invalid reservation status."}

    def approve_reservation(self):
        pending_status = ReservationStatus.objects.get(name='Pending')
        approved_status = ReservationStatus.objects.get(name='Approved')

        if self.status == pending_status:
            self.status = approved_status
            # Perform additional actions if needed
            self.save()
            return {"message": "Delivery accepted successfully.", "status": self.status.name}

        return {"message": "Cannot accept delivery. Invalid reservation status."}

    def decline_reservation(self):
        pending_status = ReservationStatus.objects.get(name='Pending')
        cancelled_status = ReservationStatus.objects.get(name='Cancelled')

        if self.status == pending_status:
            self.status = cancelled_status
            # Perform additional actions if needed
            self.save()
            # Update associated LineItems
            self.lineitem_set.filter(hold=True).update(hold=False)
            return {"message": "Delivery declined. Reservation is now in Disputed stage.", "status": self.status.name}

        return {"message": "Cannot decline delivery. Invalid reservation status."}

    def accept_delivery(self):
        delivered_status = ReservationStatus.objects.get(name='Delivered')
        borrowed_status = ReservationStatus.objects.get(name='Borrowed')
        lender_received_action = DecisionPoint.objects.get(title='lender_received_by_due_date')

        if self.stage == delivered_status:
            # Additional logic to confirm contents are correct...
            
            # Transition to "Borrowed" stage
            self.stage = borrowed_status
            # Update action_required to lender_received_by_due_date
            self.action_required = lender_received_action
            # Perform additional actions if needed
            self.save()

            # Recursively set all associated LineItems to borrowed=True
            self.lineitem.filter(hold=True).update(Lent=True)

            return {"message": "Delivery accepted successfully.", "status": self.stage.name}

        return {"message": "Cannot accept delivery. Invalid reservation status."}


    def decline_delivery(self):
        delivered_status = ReservationStatus.objects.get(name='Delivered')
        disputed_status = ReservationStatus.objects.get(name='Disputed')

        if self.status == delivered_status:
            # Additional logic for declining delivery if needed...
            
            # Transition to "Disputed" stage
            self.status = disputed_status
            # Perform additional actions if needed
            self.save()

    def cancel_reservation(self):
        delivered_status = ReservationStatus.objects.get(name='Delivered')
        cancelled_status = ReservationStatus.objects.get(name='Cancelled')

        if self.status == delivered_status:
            # If the reservation is already delivered, cannot be cancelled
            return {"message": "Cannot cancel a delivered reservation."}

        # Transition to "Cancelled" stage
        self.status = cancelled_status
        # Perform additional actions if needed
        self.save()

        return {"message": "Reservation cancelled successfully."}
    
    #this is a very rough draft, since a lot of the funcitonality here is not yet set up.
    def report_cards_lost(self, lost_inventory_ids):
        borrowed_status = ReservationStatus.objects.get(name='Borrowed')
        returned_status = ReservationStatus.objects.get(name='Returned')
        lost_status = ReservationStatus.objects.get(name='Lost')

        valid_statuses = [borrowed_status, returned_status]

        if self.status not in valid_statuses:
            return {"message": "Cannot report cards lost. Invalid reservation status."}

        if self.status == lost_status:
            return {"message": "Reservation is already in the 'Lost' stage."}

        # Additional logic for reporting cards lost if needed...

        lost_lineitems = self.lineitem_set.filter(id_inventory__in=lost_inventory_ids, borrowed=True, hold=False)
        total_lost_value = sum(lost_item.value for lost_item in lost_lineitems)

        # Transition to "Lost" stage
        self.status = lost_status
        self.save()

        return {
            "message": f"{lost_lineitems.count()} have been reported as lost. Please return all other items immediately. "
                       f"Based on your reported losses, you have a liability of {total_lost_value}. "
                       f"This liability may be greater if you have lost more than you claim to. "
                       "The lender will need to approve you to borrow items again before you can start a new reservation.",
            "status": self.status.name,
            "lost_lineitems": [{"id_inventory": lost_item.id_inventory, "value": lost_item.value} for lost_item in lost_lineitems],
            "total_lost_value": total_lost_value
        }
    
    def return_cards(self):
        borrowed_status = ReservationStatus.objects.get(name='Borrowed')
        returned_status = ReservationStatus.objects.get(name='Returned')

        if self.status == borrowed_status:
            # Additional logic for returning cards if needed...

            # Transition to "Returned" stage
            self.status = returned_status
            # Perform additional actions if needed
            self.save()

            return {"message": "Cards have been returned. Reservation is now in the 'Returned' stage. "
                               "The contents of the return still need to be verified.", "status": self.status.name}

        return {"message": "Cannot return cards. Invalid reservation status."}
    
    def lender_accepts_return(self):
        returned_status = ReservationStatus.objects.get(name='Returned')
        complete_status = ReservationStatus.objects.get(name='Complete')

        if self.status == returned_status:
            # Additional logic for lender accepting return if needed...

            # Set lent=False for all associated line items
            self.lineitem_set.filter(borrowed=True, hold=False).update(lent=False)

            # Transition to "Complete" stage
            self.status = complete_status
            # Perform additional actions if needed
            self.save()

            return {"message": "Lender has accepted the return. Reservation is now in the 'Complete' stage. "
                               "All associated line items have been updated as not lent.", "status": self.status.name}

        return {"message": "Cannot accept return. Invalid reservation status."}
    
    #this is also pretty close to pseudocode.  We are doing something a little half-baked here in adjusting some line items.
    def lender_declines_return(self, missing_inventory_ids):
        returned_status = ReservationStatus.objects.get(name='Returned')
        borrowed_status = ReservationStatus.objects.get(name='Borrowed')

        if self.status == returned_status:
            # Additional logic for lender declining return if needed...

            # Set lent=False for all associated line items that are not missing
            self.lineitem_set.filter(borrowed=True, hold=False).exclude(id_inventory__in=missing_inventory_ids).update(lent=False)

            # Transition back to "Borrowed" stage
            self.status = borrowed_status
            # Perform additional actions if needed
            self.save()

            return {"message": "Lender has declined the return. Reservation is now back in the 'Borrowed' stage. "
                               "Missing items have not been marked as not lent.", "status": self.status.name}

        return {"message": "Cannot decline return. Invalid reservation status."}
    
    def return_to_inventory(self, missing_cards):
        complete_status = ReservationStatus.objects.get(name='Complete')

        if self.status == complete_status:
            # Additional logic for returning to inventory if needed...

            # Set hold=False for all associated line items that are not missing
            self.lineitem_set.filter(borrowed=False).exclude(id_inventory__in=missing_cards).update(hold=False)

            return {"message": "Items have been returned to inventory. Hold status updated for non-missing items."}

        return {"message": "Cannot return to inventory. Invalid reservation status."}

    def __str__(self):
        return str(self.id)
        
class LineItem(models.Model):
    id_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='lineitem')
    id_inventory = models.IntegerField(default=0)
    #There is an important distinction between hold and lent.
    # Hold means that the item is unavailable to show up in searches
    # lent means that the card is currently not in the lender's posession
    lent = models.BooleanField(default=False)
    hold = models.BooleanField(default=False)
    date_created = models.DateTimeField(editable = False)
    last_updated = models.DateTimeField(editable = False)
    name = models.CharField(max_length=200)

    def __str__(self):
        id = str(self.id_inventory)
        return id
    
    def save(self, *args, **kwargs):
        '''on save, update timestamps'''
        if not self.id:
            self.date_created = timezone.now()
        self.last_updated = timezone.now()
        return super(LineItem, self).save(*args, **kwargs)

class Delinquency(models.Model):
    id_user = models.IntegerField(default=0)
    id_reservation = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)
    last_updated = models.DateTimeField('auto_now')

    def __str__(self):
        return self.id_user
    
    class Meta():
        verbose_name_plural = "Delinquencies"