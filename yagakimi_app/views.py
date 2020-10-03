from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Room
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

# Create your views here.

line_bot_api = LineBotApi(os.environ['LINE_TOKEN'])


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


@csrf_exempt
def push_room_id_to_line(request):

    if request.method == 'POST':
        request_json = json.loads(request.body)
        line_messsage = request_json["line_messsage"]
        line_bot_api.push_message(
            os.environ['ROOM_ID'], TextSendMessage(text=line_messsage))
        return JsonResponse(data={"message": "successfully pushed line message"})
    else:
        return JsonResponse(data={"message": "only POST is acceptalbe"}, status=400)
