from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User

# Create your views here.


@csrf_exempt
def user_create(request):

    if request.method == 'POST':
        request_json = json.loads(request.body)
        user = User()
        user.uuid = request_json["uuid"]
        user.name = ""
        user.twitter_id = ""
        user.password = ""
        user.save()
        return JsonResponse(data={"message": "successfully added a new user"})
    else:
        return JsonResponse(data={"message": "only POST is acceptalbe"}, status=400)
