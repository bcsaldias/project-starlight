from django.conf.urls import url

from . import views


app_name = 'user'
urlpatterns = [
    url(r'ranking/$', views.ranking, name="ranking"),
    url(r'login/$', views.login, name="login"),
    url(r'register/$', views.register, name="register"),
    url(r'logout/$', views.logout, name="logout"),
    url(r'(?P<username>[\w]+)/$', views.profile, name="profile"),
    url(r'(?P<username>[\w]+)/dashboard/$', views.dashboard, name="dashboard"),
    url(r'(?P<username>[\w]+)/edit-profile/$', views.edit_profile, name="edit_profile"),
]
