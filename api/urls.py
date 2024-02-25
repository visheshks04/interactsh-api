from django.urls import path
from .views import *

urlpatterns = [
    path("getURL/", get_url, name="main-view"),
    path("getInteractions/", get_interactions, name="main-view"),
]
