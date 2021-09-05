

from django.urls import path
from . import views
urlpatterns = [
    path('', views.searchEngine.as_view(),name="index")]