from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GirlsLove


@csrf_exempt
def index(request):
    if request.method == 'GET':
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
    elif request.method == 'POST':
        return JsonResponse(data={"message": "nothing done"})
    else:
        return JsonResponse(data={"message": "unexpetected http method"}, status=400)
