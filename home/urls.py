from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^usuario/(?P<usuario_other>.+)$', views.Usuario_page),
    url(r'^upload_image/$', views.Upload_image)
]
