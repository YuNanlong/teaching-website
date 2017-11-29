from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^detail', views.teach_detail, name="teach_detail"), # Better to add teach_ prefix to avoid duplicate names
]