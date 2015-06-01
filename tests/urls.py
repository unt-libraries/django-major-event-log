from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^major-event-log/', include('major_event_log.urls',
        namespace="major-event-log"))
]
