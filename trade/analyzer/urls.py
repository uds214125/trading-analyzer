# from django.contrib import admin
# from django.urls import path, include
# from rest_framework import routers
from analyzer.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^api/v1/', AnalyzerList.as_view()),
]
