from django.conf.urls import url
from .views import TaskList, TaskCreate, TaskUpdate


urlpatterns = [
    url(r'create/$', TaskCreate.as_view(), name='task-create'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    url(r'^$', TaskList.as_view(), name='task-list'),
]
