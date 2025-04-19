from django.urls import path

from .views import *

urlpatterns = [
    path("<str:challenge>", DoItFast.as_view(), name="do-it-fast"),
]
