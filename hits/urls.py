from django.conf.urls import url

from . import views


app_name = 'hits'
urlpatterns = [
    url(r'^$', views.hits_list, name="list"),
    url(r'learn-catalina/$', views.learn, name="learn"),
    url(r'random$', views.hits_random, name="random"),
    url(r'([0-9.]*)/$', views.hits_detail, name="detail"),
    #url(r'([0-9.]*)/data$', views.hits_data, name="data"),
]
