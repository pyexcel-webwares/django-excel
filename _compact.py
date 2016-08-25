try:
    from django.http import JsonResponse
except ImportError:
    from django.http import HttpResponse
    import json

    def JsonResponse(data):
        return HttpResponse(json.dumps(data),
                            content_type="application/json")
