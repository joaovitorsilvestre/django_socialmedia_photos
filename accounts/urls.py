from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^login/$', views.Login, name='login'),
    url(r'^login_ajax/$', views.Login_ajax ),
    url(r'^register/$', views.Register, name='register'),
    url(r'^logout/$', views.Logout),
    url(r'^activate/(?P<key>.+)/$', views.Activate),
]
