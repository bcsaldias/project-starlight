from django.conf.urls import url

from . import views

app_name = 'macho'
urlpatterns = [
    url(r'^$', views.macho_list, name="list"),
    url(r'(?P<macho_id>[0-9\.]+)/$', views.macho_detail, name="detail"),
]
