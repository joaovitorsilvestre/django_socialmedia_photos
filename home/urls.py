from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^$', views.Home),
    url(r'^usuario/(?P<nome_usuario_page>.+)$', views.Usuario_page)
]
