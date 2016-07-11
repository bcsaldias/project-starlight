from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'about/$', views.about, name="about")
    # url(r'^$', views.IndexView.as_view(), name="index"),
    # url(r'about/$', views.AboutView.as_view(), name="about"),
]
