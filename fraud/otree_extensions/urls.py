from django.urls import path, include, re_path
from fraud.views import UnblockView,UnblockFinalResultsView

urlpatterns = [
    path(UnblockView.url_pattern, UnblockView.as_view(), name=UnblockView.url_name),
    path(UnblockFinalResultsView.url_pattern, UnblockFinalResultsView.as_view(), name=UnblockFinalResultsView.url_name),
]
