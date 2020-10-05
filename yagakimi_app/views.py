import json
import os
import datetime
from janome.tokenizer import Tokenizer
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
        uuid = request_json["uuid"]
        if User.objects.filter(uuid=uuid).count() != 0:
            return JsonResponse(data={"message": "This UUID is already registered."})

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


@csrf_exempt
def user_add_twitter_id(request):
    if request.method == 'POST':
        request_json = json.loads(request.body)
        uuid = request_json["uuid"]
        twitter_id = request_json["twitter_id"]
        try:
            user = User.objects.get(uuid=uuid)
        except Exception:
            return JsonResponse(data={"message": "internal server error"},
                                status=500)
        user.twitter_id = twitter_id
        user.save()

        return JsonResponse(data={"message": "successfully added a twitter_id"})
    else:
        return JsonResponse(data={"message": "only POST is acceptalbe"}, status=400)


@csrf_exempt
def calculate(request):
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body)
            webrtc_room_id = request_json["webrtc_room_id"]
            all_texts = Text.objects.all().filter(webrtc_room_id=webrtc_room_id)
            t = Tokenizer()

            relax_count = 0
            all_count = len(all_texts)
            if all_count == 0:
                return JsonResponse(data={"relaxing_topics": ["明日の天気", "昨日のテレビ"], "relax_rate": 0.6})

            # relaxing_topics → is_ralaxのときのtextの全部もしくは一部の集合
            relaxing_topics = []
            di = {}
            for text in all_texts:
                print(type(text.watson_response))
                print((text.watson_response))
                watson_response = json.loads(text.watson_response)
                watson_response = watson_response["classes"]
                postive = 0
                negative = 0
                score = 0
                for c in watson_response:
                    if c["class_name"] == "postive":
                        postive = c["confidence"]
                    if c["class_name"] == "negative":
                        negative = c["confidence"]
                scale = 0
                if postive > negative:
                    score = postive
                    if text.is_relax:
                        scale = 2
                    else:
                        scale = -2

                else:
                    score = negative
                    if text.is_relax:
                        scale = 1
                    else:
                        scale = -1

                for word in t.tokenize(text.text):
                    if "名詞" in word.part_of_speech:
                        if word.surface not in di:
                            di[word.surface] = score * scale
                        else:
                            di[word.surface] = di[word.surface] + score * scale

                if text.is_relax:
                    relax_count += 1
            relaxing_rate = (relax_count + 1)/(all_count + 1)
            print(di)
            di = sorted(di.items(), key=lambda x: -x[1])
            max_value = di[0][0]
            second_value = di[1][0]
            relaxing_topics = [max_value, second_value]
            if len(relaxing_topics) == 0:  # 現状は、いい感じのトピックがない場合はデフォルト値を返す
                relaxing_topics.append("お天気")

            return JsonResponse(data={"relaxing_topics": relaxing_topics, "relax_rate": relaxing_rate})
        except:
            return JsonResponse(data={"relaxing_topics": ["最近ハマってること", "昨日のテレビ"], "relax_rate": 0.6})

    else:
        return JsonResponse(data={"message": "only POST is acceptalbe"}, status=400)
