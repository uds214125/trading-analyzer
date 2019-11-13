
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AnalyzerSerializer
from .models import Analyzer

from django.db.models import F,Avg,Sum

class AnalyzerList(APIView):
    """
        Get API endpoint which allows get all records, get by filter ( or query)
    """
    # queryset = User.objects.all()
    # serialize_class = AnalyzerSerializer
    def get(self, request):

        if request.method == 'GET':
            queryset = Analyzer.objects.all()
            Date1 = request.GET.get('start', None)
            Date2 = request.GET.get('end', None)
            # print("=========Date2 ===", type(Date2))
            if Date1 is not None and Date2 is not None:

                queryset = queryset.filter(Open__gt=F('Close')).filter(Date__gte=Date1, Date__lte=Date2)
                print("range and > queryset==========: ",str(queryset.query))
                serializer_class = AnalyzerSerializer(queryset,many=True)
                return Response(serializer_class.data)
            else:
                print("Get all record==========:")
                queryset = Analyzer.objects.all()
                serializer_class = AnalyzerSerializer(queryset,many=True)
                return Response(serializer_class.data)

    def post(self,request):
        if request.method == 'POST':
            serializer = AnalyzerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)