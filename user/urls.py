from django.conf.urls import url

from . import views


app_name = 'user'
urlpatterns = [
    url(r'login/$', views.login_user, name="login"),
    url(r'register/$', views.register, name="register"),
    url(r'logout/$', views.logout_user, name="logout"),

    url(r'ranking/$', views.ranking, name="ranking"),

    url(r'(?P<username>[\w]+)/$', views.profile, name="profile"),
    url(r'(?P<username>[\w]+)/votes$', views.votes, name="votes"),
    # url(r'(?P<username>[\w]+)/activities$', views.activities, name="activities"),
    # url(r'(?P<username>[\w]+)/saved$', views.saved, name="saved"),
    # url(r'(?P<username>[\w]+)/edit-profile/$', views.edit_profile, name="edit_profile"),
    # url(r'(?P<username>[\w]+)/update-password/$', views.update_password, name="update_passowrd"),
]
