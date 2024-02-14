# sylvan-safekeeper
database for sylvan library and backend business logic

this is the backend for the project found here: https://github.com/anthony-devarti/sylvan-library

## A very early db diagram
![sl diagram](https://github.com/anthony-devarti/sl-db/assets/98314025/9a8ecd24-c08b-454c-b49a-ee8d8799a65d)


## Notes on backend:
<ul>We want cards to be reserved immediately when a user adds them to their basket
  <li>Make sure if this happens, a card cannot be reserved forever</li>
  <li>This means that LineItem is updated immediately onClick of Reserve button </li></ul>

## Keeping packages synchronized across virtual machines
  During each session on gitpod, or for each user, it is necessary to reinstall all packages for this project.  To avoid us falling out of sync with each other and installing different sets of packages across different environments, I have set up the requirements.txt file.  When you fire up a gitpod env, just run 
  pip install requirements.txt 
  so all of the packages are installed at once.  If a new package needs to be added, simply add it to the requirements.txt file by running 
  pip freeze > requirements.txt

## Data Models Fields
  Want to add a field to a Model?  That's likely to happen a lot.  Here's a list of the default field data types that Django has for us to choose from:
  https://www.geeksforgeeks.org/django-model-data-types-and-fields-list/
  When you change a model, don't forget to python manage.py makemigrations then python manage.py migrate
  If you are adding a non-nullable field to a model, django will force you to either make the field nullable, or define something to set the field to so previous entries are not nullable.  This will happen even if the model is empty, because migrations can be rolled back and applied piecemeal.  Honestly, you should probably just have some default option for most fields.

  ### Want to make a whole new model?  
  Start by making a model in library/models.py  You can follow the pattern of the models in there  Models should be named in the singular form.  For example, a model for Peanuts will be called Peanut
  Next, you want to move to serializers.py in the same dir and make a serializer for it  PeanutSerializer.  You need to import the Peanut Model, here.
  Next, you want to move to views.py and create a viewset for it PeanutViewset.  You need to import the Peanut Model AND the PeanutSerializer, here.
  Then you want to move to urls.py and register this view with the router. peanut.  you will need to import the PeanutViewSet, here.
  Dont forget to register this view with the admin portal so we can easily mess with it if needed.

  Use the serializers, it makes sure that every endpoint we create acts predictably and the same as the others.  Django docs help
# Reservation Workflow Documentation

## Overview

The reservation workflow involves the lifecycle of a reservation, from its creation to completion. This document outlines the various stages and actions associated with the reservation process.

## Reservation Stages

### 1. Unrequested
- **Description:** The initial stage when a borrower creates a reservation but has not submitted it.
- **Actions:**
  - `submit_reservation`: Submits the reservation, transitioning it to the "Pending" stage.

### 2. Pending
- **Description:** The reservation is awaiting approval from the lender.
- **Actions:**
  - `approve_reservation`: Approves the reservation, transitioning it to the "Approved" stage.
  - `decline_reservation`: Declines the reservation, transitioning it to the "Cancelled" stage.

### 3. Approved
- **Description:** The lender has approved the reservation, and the cards are not yet in the borrower's possession.
- **Actions:**
  - `accept_delivery`: Confirms delivery and transitions to the "Borrowed" stage.

### 4. Delivered
- **Description:** The borrower has possession of the reservation but has not yet confirmed the contents.
- **Actions:**
  - `accept_delivery`: Confirms the contents, transitioning to the "Borrowed" stage.
  - `decline_delivery`: Raises a dispute and transitions to the "Disputed" stage.

### 5. Borrowed
- **Description:** The borrower has possession of the reservation, and the return date has not passed.
- **Actions:**
  - `return_cards`: Initiates the return process, transitioning to the "Returned" stage.
  - `report_cards_lost`: Reports lost cards and transitions to the "Lost" stage.
  - `return_to_inventory`: Returns cards to inventory if the reservation is complete.

### 6. Returned
- **Description:** The reservation has been returned, and the lender needs to verify the contents.
- **Actions:**
  - `lender_accepts_return`: Accepts the return, transitioning to the "Complete" stage.
  - `lender_declines_return`: Declines the return, transitioning back to the "Borrowed" stage.

### 7. Complete
- **Description:** The reservation is complete, and all cards are confirmed as returned and in good condition.

### 8. Lost
- **Description:** Cards are reported as lost, and the borrower has a liability.

### 9. Disputed
- **Description:** The borrower disputes the reservation, and the lender needs to address the issues.

### 10. Late
- **Description:** The reservation is overdue, and the borrower has not yet returned the items.

### 11. Delinquent
- **Description:** The borrower has received a delinquent strike, and the lender may disallow future reservations.

## Actions

- `submit_reservation`: Submits the reservation for approval.
- `approve_reservation`: Lender approves the reservation.
- `decline_reservation`: Lender declines the reservation.
- `accept_delivery`: Confirms delivery of the reservation.
- `decline_delivery`: Declines the delivery, raising a dispute.
- `cancel_reservation`: Cancels the reservation.
- `report_cards_lost`: Reports cards as lost.
- `return_cards`: Initiates the return process.
- `lender_accepts_return`: Lender accepts the returned items.
- `lender_declines_return`: Lender declines the return.
- `return_to_inventory`: Returns items to inventory.

## Notes

- Ensure proper validation and authorization for each action.
- Follow the recommended workflow to maintain consistency.
- Additional business logic may be added as needed.

## Unban Git Probe everywhere #FreeProbing