from django.test import TestCase
from .models import Case, ProblemLineItem, ReservationStatus, DecisionPoint, Reservation, LineItem
from .serializers import ReservationSerializer
# import datetime
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Reservation, ReservationStatus, DecisionPoint
from datetime import datetime, timedelta

class CaseModelTest(TestCase):
    def setUp(self):
        # Create a test reservation status if it doesn't exist
        self.disputed_status, created = ReservationStatus.objects.get_or_create(name='Disputed')
        self.completed_status, created = ReservationStatus.objects.get_or_create(name="Complete")

        # Create a test decision point if it doesn't exist
        self.lender_corrects_decision, created = DecisionPoint.objects.get_or_create(
            title='lender_corrects',
            description='Test Description',
            terminal=False,
            destination_on_decline=self.completed_status,
            destination_on_success=self.disputed_status,
            accept_button='Accept',
            decline_button='Decline',
            responsibility='borrower',
            header='Test Header',
            button_text='Address Action'
        )
        #create a test reservation
        self.test_reservation = Reservation.objects.create(
            id_user=1,
            stage=self.disputed_status,
            action_required=self.lender_corrects_decision,
            return_date=timezone.now() + timezone.timedelta(days=7)
        )

        # Set up test problem line items
        self.test_line_item_1 = LineItem.objects.create(
            id_reservation=self.test_reservation,
            name="Test Item 1",
            hold=True,
            date_created=timezone.now(),
            last_updated=timezone.now()
        )

        self.test_line_item_2 = LineItem.objects.create(
            id_reservation=self.test_reservation,
            name="Test Item 2",
            hold=True,
            date_created=timezone.now(),
            last_updated=timezone.now()
        )

    def test_create_case(self):
    # Use the existing setup code to create test reservation status and decision point
        self.setUp()

        # Access the existing reservation and line items from the setup
        test_reservation = self.test_reservation
        test_line_item_1 = self.test_line_item_1
        test_line_item_2 = self.test_line_item_2
        test_items = [
            {"id": test_line_item_1.id, "issue": "Some issue for item 1"},
            {"id": test_line_item_2.id, "issue": "Some issue for item 2"}
        ]

        # Call create_case on the reservation instance
        response = test_reservation.open_case(
            id_user=1,
            items=test_items,
            note="Test Note"
        )

        #Extract the case id for tests
        case_id = response.get("case_id")

        # Check if the case was created
        self.assertTrue(Case.objects.filter(id_reservation=self.test_reservation.id).exists())

        # check ProblemLineItem count
        problem_line_items_count = ProblemLineItem.objects.filter(id_case=case_id).count()
        self.assertEqual(problem_line_items_count, len(test_items))
