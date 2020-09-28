import os
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
from requests.auth import HTTPBasicAuth


CONFIG = {
    'user': 'apikey',
    'pass': os.environ['WATSON_PASSWORD'],
    'headers': {'Content-type': 'application/json'},
    'url': 'https://api.jp-tok.natural-language-understanding.watson.cloud.ibm.com/instances/8674a94a-20ad-42ed-b0ce-3321526d6231/v1/analyze',
    'params': {'version': '2018-11-16'},
    'data': {
        "text": "",
        "features": {
            "categories": {},
            "keywords": {
                "emotion": True
            },
            "entities": {},
            "concepts": {
                "limit": 3
            },
        },
    }
}

YAGAKIMI_WIKIPEDIA_TEXT = '『やがて君になる』は、仲谷鳰による日本の漫画。略称は『やが君』。誰のことも特別に思えない少女と、自分自身のことが嫌いなために他人からの好意を受け入れられない少女の2人を軸とした百合漫画である。'


@csrf_exempt
def index(request):
    if request.method != 'GET' and request.method != 'POST':
        return JsonResponse({})

    if request.method == 'GET':
        CONFIG['data']["text"] = YAGAKIMI_WIKIPEDIA_TEXT
    else:  # POSTのとき
        request_json = json.loads(request.body)
        CONFIG['data']["text"] = request_json["text"]

    r = requests.post(CONFIG['url'],
                      params=CONFIG['params'],
                      data=json.dumps(CONFIG['data']),
                      headers=CONFIG['headers'],
                      auth=HTTPBasicAuth(CONFIG['user'], CONFIG['pass']))

    return JsonResponse(
        data={"message": "analysis result from watson",
              "data": json.loads(r.text)}
    )
