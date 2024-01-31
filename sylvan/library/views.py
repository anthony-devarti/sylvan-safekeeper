from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from library.models import ReservationStatus, LineItem, Reservation, Delinquency, DecisionPoint
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
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
    filterset_fields = ['hold', 'id_inventory']

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows reservations to be viewed or edited
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

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