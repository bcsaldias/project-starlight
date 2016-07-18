from django.conf.urls import url

from . import views


app_name = 'hits'
urlpatterns = [
    url(r'^$', views.hits_list, name="list"),
    url(r'(?P<hits_id>[0-9\.]+)/$', views.hits_detail, name="detail"),
]
