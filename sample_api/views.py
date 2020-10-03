from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GirlsLove
import json


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
        request_json = json.loads(request.body)

        girls_love = GirlsLove()
        girls_love.follower_name = request_json['follower_name']
        girls_love.followee_name = request_json['followee_name']
        girls_love.save()

        return JsonResponse(data={"message":
                                  "successfully added a new girls love"})
    else:
        return JsonResponse(data={"message": "unexpetected http method"}, status=400)
