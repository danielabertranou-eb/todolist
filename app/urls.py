from django.conf.urls import url
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete


urlpatterns = [
    url(r'create/$', TaskCreate.as_view(), name='task-create'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    url(r'delete/(?P<pk>[0-9]+)/$', TaskDelete.as_view(), name='task-delete'),
    url(r'^$', TaskList.as_view(), name='task-list'),
]
