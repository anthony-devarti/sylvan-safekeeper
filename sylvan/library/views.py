from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from library.models import ReservationStatus
from library.serializers import ReservationStatusSerializer

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