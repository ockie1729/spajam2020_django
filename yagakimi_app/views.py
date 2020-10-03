import json
import os
import datetime

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi
from linebot.models import TextSendMessage

from asari.api import Sonar

from .models import User, Text


line_bot_api = LineBotApi(os.environ['LINE_TOKEN'])
sonar = Sonar()  # 極性分析器


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
        line_message = request_json["line_message"]
        line_bot_api.push_message(
            os.environ['ROOM_ID'], TextSendMessage(text=line_message))
        return JsonResponse(data={"message": "successfully pushed line message"})
    else:
        return JsonResponse(data={"message": "only POST is acceptalbe"}, status=400)


@csrf_exempt
def topic_register_text(request):

    if request.method == 'POST':
        api_call_time = datetime.datetime.now()  # モデルのcreated_atに使用

        request_json = json.loads(request.body)
        request_text = request_json['text']
        request_webrtc_room_id = request_json['webrtc_room_id']
        request_uuid = request_json['uuid']
        request_is_relax_str = request_json['is_relax']  # TODO 現在はまだ使用せず

        # asariで極性分析を実行
        asari_result = sonar.ping(text=request_text)

        # Textモデルを作成し，値を保存
        new_text = Text()
        new_text.text = request_text
        new_text.watson_response = json.dumps(asari_result)  # TODO フィールド名を修正
        new_text.created_at = api_call_time
        new_text.uuid = request_uuid
        new_text.webrtc_room_id = request_webrtc_room_id
        # new_text.tokenized_text  # TODO 未実装
        new_text.save()

        return JsonResponse(
            data={"message": "successfully registered a text message",
                  "watson_response": asari_result}  # TODO key名を修正
        )
    else:
        return JsonResponse(data={"message": "only POST is acceptalbe"},
                            status=400)
