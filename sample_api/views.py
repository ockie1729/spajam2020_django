from django.http import JsonResponse
from .models import GirlsLove


def index(request):
    girls = GirlsLove.objects.all()

    content = []
    for girl in girls:
        girl_dict = {}
        girl_dict["follower_name"] = girl.follower_name
        girl_dict["followee_name"] = girl.followee_name
        content.append(girl_dict)

    response = {}
    response["message"] = "OK"
    response["content"] = content
    return JsonResponse(data=response)
