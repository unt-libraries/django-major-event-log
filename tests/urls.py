from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('major-event-log/', include(('major_event_log.urls', 'major-event-log'),
         namespace="major-event-log"))
]
