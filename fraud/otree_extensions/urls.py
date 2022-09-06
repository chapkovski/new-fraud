from django.urls import path, include, re_path
from fraud.views import UnblockView

urlpatterns = [
    path(UnblockView.url_pattern, UnblockView.as_view(), name=UnblockView.url_name),
]
