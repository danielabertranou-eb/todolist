from django.conf.urls import url, include
from django.contrib import admin
from app.views import Login, Logout, EventList


urlpatterns = [
    url(r'events/', include('app.urls')),
    url(r'accounts/logout/$', Logout.as_view(), name='logout'),
    url(r'accounts/login/$', Login.as_view(), name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', EventList.as_view(), name='event-list'),
    url('', include('social_django.urls', namespace='social')),
]
