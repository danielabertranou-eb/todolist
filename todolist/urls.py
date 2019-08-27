from django.conf.urls import url, include
from django.contrib import admin
from app.views import Login, Logout


urlpatterns = [
    url(r'accounts/logout/$', Logout.as_view(), name='logout'),
    url(r'accounts/login/$', Login.as_view(), name='login'),
    url(r'tasks/', include('app.urls')),
    url(r'^admin/', admin.site.urls),
]
