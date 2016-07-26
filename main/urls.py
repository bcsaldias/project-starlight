from django.conf.urls import url, handler404

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'about/$', views.about, name="about"),
    url(r'learn/$', views.learn, name="learn"),
]
handler404 = 'main.views.my_page_not_found'
