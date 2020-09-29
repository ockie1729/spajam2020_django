from django.http import JsonResponse
from .models import GirlsLove


def index(request):
    girls = GirlsLove.objects.all()

    return JsonResponse(data=girls)
