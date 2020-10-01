from django.http import JsonResponse


def index(request):
    return JsonResponse(
        data={'message': 'Hello, world from API server index, deployed with GitHub actions triggered by PullRequest'}
    )
