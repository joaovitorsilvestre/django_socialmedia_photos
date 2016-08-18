from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^search/(?P<searchString>\w*)$', views.Search),
    url(r'^sendfiles/$', views.SendFiles),
    url(r'^isfriend/(?P<user>\w*)$', views.IsFriend),
    url(r'^requestfriend/(?P<user>\w*)$', views.RequestFriend),
    url(r'^requesttome/$', views.RequestToMe),
    url(r'^acceptrequest/(?P<user>\w*)$', views.AcceptRequest),
    url(r'^getselfimages/$', views.GetSelfImages),
    url(r'^getfriends/$', views.GetFriends)
]
