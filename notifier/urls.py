from django.urls import path
from notifier import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/webhook/twitter', views.listener, name='listener')
]
