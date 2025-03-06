from django.http import JsonResponse
from django.urls import reverse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the Proximity-Based Marketing API",
        "documentation": {
            "swagger": request.build_absolute_uri(reverse('swagger-ui')),
            "redoc": request.build_absolute_uri(reverse('redoc')),
            "openapi_schema": request.build_absolute_uri(reverse('schema')),
        },
        "endpoints": {
            "Beacons": request.build_absolute_uri('/api/v1/beacons/'),
            "Active Beacons": request.build_absolute_uri('/api/v1/beacons/active'),
            "Beacons Message Count": request.build_absolute_uri('/api/v1/beacons/messages/count/'),
            "Advertisements": request.build_absolute_uri('/api/v1/advertisements/'),
            "Cached Advertisements": request.build_absolute_uri('/api/v1/advertisements/cached_ad'),
            "Advertisement Assignments": request.build_absolute_uri('/api/v1/advertisements/assignments'),
            "Logs": request.build_absolute_uri('/api/v1/logs/'),
            "Messages": request.build_absolute_uri('/api/v1/messages/'),
            "Authentication": {
                "Obtain Token": request.build_absolute_uri(reverse('token_obtain_pair')),
                "Refresh Token": request.build_absolute_uri(reverse('token_refresh')),
            }
        }
    })
