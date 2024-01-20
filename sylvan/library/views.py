from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from library.models import ReservationStatus, LineItem, Reservation, Delinquency
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from library.serializers import UserSerializer, ReservationStatusSerializer, LineItemSerializer, ReservationSerializer, DelinquencySerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

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