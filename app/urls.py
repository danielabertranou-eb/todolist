from django.conf.urls import url
from .views import (
    EventList,
    TaskList,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    mark_as_done,
)


urlpatterns = [
    url(r'^$', EventList.as_view(), name='event-list'),
    url(r'(?P<event_id>[0-9]+)/tasks/create/$', TaskCreate.as_view(), name='task-create'),
    url(r'(?P<event_id>[0-9]+)/tasks/update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    url(r'(?P<event_id>[0-9]+)/tasks/delete/(?P<pk>[0-9]+)/$', TaskDelete.as_view(), name='task-delete'),
    url(r'(?P<event_id>[0-9]+)/tasks/done/(?P<pk>[0-9]+)/$', mark_as_done, name='task-done'),
    url(r'(?P<event_id>[0-9]+)/tasks/', TaskList.as_view(), name='task-list'),
]
    