from analyzer.views import *
from django.conf.urls import url
# from django.urls import path, include
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('api', AnalyzerList)

urlpatterns = [
    # path('', include(router.urls) ),
    url(r'^api/v1/', AnalyzerList.as_view()),
]
