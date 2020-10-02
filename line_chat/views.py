from django.shortcuts import render
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
import os
line_bot_api = LineBotApi(os.environ['LINE_TOKEN'])


@csrf_exempt
def index(request):
    logger = logging.getLogger('development')
    logger.info('index!')

    try:
        line_bot_api.push_message(
            'your_group_or_user_id', TextSendMessage(text='百合は良いぞ'))
    except LineBotApiError as e:
        print("error")
    return JsonResponse(data={}, status=200)


def push_message(request, user_num):

    return


@csrf_exempt
def webhook(request):
    print(request.body.decode('utf-8'))
    return JsonResponse({}, status=200)
