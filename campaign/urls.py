from django.urls import path
from . import views
from .api import advertisements_view, beacons_view


urlpatterns = [
    path('api/beacons/', beacons_view.beacons_list, name='beacons_list'),
    path('api/beacons/<uuid:uuid>', beacons_view.beacons_detail, name='beacons_detail'),
    path('api/beacons/search', beacons_view.beacons_search, name='beacons_search'),
    path('api/beacons/active', beacons_view.active_beacons, name='active_beacons'),
    path('api/beacons/count', beacons_view.beacons_count,  name='count_beacons'),

    # path('api/beacons', beacons_view.AllBeacons.as_view(), name='all_beacons'),

    path('api/advertisements/', advertisements_view.advertisements_list, name='advertisement_list'),
    path('api/advertisements/<uuid:uuid>', advertisements_view.advertisements_detail, name='advertisement_detail'),
    path('api/advertisements/active', advertisements_view.advertisements_active, name='advertisements_active')

]