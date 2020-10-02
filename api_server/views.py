from django.http import JsonResponse

import logging


def index(request):
    logger = logging.getLogger(__name__)
    logger.info("hello world")
    return JsonResponse(
        data={'message': 'Hello, world from API server index, deployed with GitHub actions triggered by PR merge'}
    )
