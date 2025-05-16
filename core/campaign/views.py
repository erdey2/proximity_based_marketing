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
            "Users": request.build_absolute_uri('/api/v1/users/'),
            "Beacons": request.build_absolute_uri('/api/v1/beacons/'),
            "Active Beacons": request.build_absolute_uri('/api/v1/beacons/active'),
            "Beacons Count": request.build_absolute_uri('/api/v1/dashboards/beacons-count/'),
            "Beacon with Ads": request.build_absolute_uri('/api/v1/beacons/advertisements/'),
            "Beacon Location List": request.build_absolute_uri('/api/v1/beacons/location'),
            "Beacon Location Count": request.build_absolute_uri('/api/v1/dashboards/location-count/'),
            "Beacons Message Count": request.build_absolute_uri('/api/v1/dashboards/message-count'),

            "Advertisements": request.build_absolute_uri('/api/v1/advertisements/'),
            "Advertisement Assignments": request.build_absolute_uri('/api/v1/assignments/'),
            "Advertisement assigned to Beacon": request.build_absolute_uri('/api/v1/advertisements/beacons/'),

            "Logs": request.build_absolute_uri('/api/v1/logs/'),
            "Logs Count": request.build_absolute_uri('/api/v1/dashboards/log-count/'),

            "Messages": request.build_absolute_uri('/api/v1/beacon-messages/'),
            "Messages Count": request.build_absolute_uri('/api/v1/dashboards/message-count'),
        }
    })
