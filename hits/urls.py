from django.conf.urls import url

from . import views


app_name = 'hits'
urlpatterns = [
    url(r'^$', views.hits_list, name="list"),
    url(r'learn-hits/$', views.learn, name="learn"),
    url(r'random$', views.hits_random, name="random"),
    url(r'(?P<hits_id>[\w]+)/$', views.hits_detail, name="detail"),
    url(r'(?P<hits_id>[\w]+)/data$', views.hits_data, name="data"),
]
