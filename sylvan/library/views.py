from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from library.models import ReservationStatus, LineItem, Reservation, Delinquency, DecisionPoint
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from library.serializers import UserSerializer, ReservationStatusSerializer, LineItemSerializer, ReservationSerializer, DelinquencySerializer, DecisionPointSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token


# Create your views here.
def index(request):
    return HttpResponse('This is the library index.')

# @csrf_exempt
def status_list(request):
    """
    List all statuses.
    """
    if request.method == 'GET':
        queryset = ReservationStatus.objects.all()
        serializer = ReservationStatusSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    # return HttpResponse('touching the status list')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
                return JsonResponse({'message': 'Login successful', 'csrf_token': get_token(request), 'user': user_data})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        try:
            # Perform logout
            logout(request)

            return JsonResponse({'message': 'Logout successful'})
        except Exception as e:
            # Handle any potential exceptions during logout
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReservationStatusViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows reservation statuses to be viewed or edited
    """
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer

class LineItemViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows line items to be viewed or edited
    """
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
    # filter_backends=['DjangoFilterBackend']
    filterset_fields = ['hold', 'id_inventory', 'id_reservation']

    # customize creating a line item so it returns the full basket 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Assuming you have the new_line_item created
        related_line_items = LineItem.objects.filter(hold=True, id_reservation=serializer.data['id_reservation'])

        # Serialize the related line items
        related_line_items_data = LineItemSerializer(related_line_items, many=True).data

        headers = self.get_success_headers(serializer.data)

        return Response(related_line_items_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'])
    def remove_from_basket(self, request, pk=None):
        line_item = self.get_object()
        line_item.hold = False
        line_item.save()

        # Assuming you have the updated_line_item
        updated_line_items = LineItem.objects.filter(hold=True, id_reservation=line_item.id_reservation)

        # Serialize the updated line items
        updated_line_items_data = LineItemSerializer(updated_line_items, many=True).data

        return Response(updated_line_items_data)

    # this exclusively is used to release all items associated with a single reservation from hold 
    @action(detail=False, methods=['post'])
    def release_line_items(self, request):
        id_reservation = request.data.get('id_reservation')

        # Validate id_reservation
        if id_reservation is None:
            return Response({'error': 'id_reservation is required'}, status=400)

        # Update line items with the provided id_reservation
        line_items = LineItem.objects.filter(id_reservation=id_reservation)
        line_items.update(hold=False, lent=False)

        return Response({'success': 'All associated line items have been released.'})

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows reservations to be viewed or edited
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filterset_fields = ['id_user', 'stage']

    @action(detail=True, methods=['post'])
    def submit_reservation(self, request, pk=None):
        reservation = self.get_object()

        try:
            # Get relevant data from the request payload
            note = request.data.get('note', '')
            pickup_method = request.data.get('pickup_method', '')
            return_date = request.data.get('return_date', '')
            pickup_date = request.data.get('pickup_date', '')

            # Call the submit method with the relevant data
            response_data = reservation.submit(
                note=note,
                pickup_method=pickup_method,
                return_date=return_date,
                pickup_date=pickup_date
            )

            # Constructing the HTTP response
            return Response({
                'message': response_data['message'],
                'status': response_data['status'],
                'lineitems': response_data['lineitems'],
            }, status=200)

        except Exception as e:
            # Handling exceptions and returning an error response
            return Response({'error': str(e)}, status=400)
    
    @action(detail=True, methods=['post'])
    def approve_reservation(self):
        reservation = self.get_object()

        try:
            response_data = reservation.approve_reservation()

            # Constructing the HTTP response
            return Response({
                'message': response_data['message'],
                'status': response_data['status'],
            }, status=200)

        except Exception as e:
            # Handling exceptions and returning an error response
            return Response({'error': str(e)}, status=400)
        
    @action(detail=True, methods=['post'])
    def decline_reservation(self, request, pk=None):
        reservation = self.get_object()

        try:
            response_data = reservation.decline_reservation()

            # Constructing the HTTP response
            return Response({
                'message': response_data['message'],
                'status': response_data['status'],
            }, status=200)

        except Exception as e:
            # Handling exceptions and returning an error response
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def return_cards(self, request, pk=None):
        reservation = self.get_object()

        try:
            response_data = reservation.return_cards()

            # Constructing the HTTP response
            return Response({
                'message': response_data['message'],
                'status': response_data['status'],
            }, status=200)

        except Exception as e:
            # Handling exceptions and returning an error response
            return Response({'error': str(e)}, status=400)
        
class DelinquencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows delinquencies to be viewed or edited.
    Delinquencies can be marked as invalid, but should never be deleted.
    """
    queryset = Delinquency.objects.all()
    serializer_class = DelinquencySerializer

class DecisionPointViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that shows DecisionPoints Along the workflow
    """
    queryset = DecisionPoint.objects.all()
    serializer_class = DecisionPointSerializer