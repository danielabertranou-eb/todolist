from django.conf.urls import url
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, mark_as_done


urlpatterns = [
    url(r'create/$', TaskCreate.as_view(), name='task-create'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    url(r'delete/(?P<pk>[0-9]+)/$', TaskDelete.as_view(), name='task-delete'),
    url(r'done/(?P<pk>[0-9]+)/$', mark_as_done, name='task-done'),
    url(r'^$', TaskList.as_view(), name='task-list'),
]
