from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^$', views.Index),
    url(r'^ownpage$', views.OwnPage),
    url(r'^userpage/', views.UserPage),
    url(r'^defaultpage/$', views.DefaultPage)
]
