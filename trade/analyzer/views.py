
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

from django.db.models import F,Avg

class AnalyzerList(APIView):
    """
        Get API endpoint which allows get all records, get by filter ( or query)
    """
    def get(self, request):

        if request.method == 'GET':
            queryset = Analyzer.objects.all()
            Date1 = request.GET.get('start', None)
            Date2 = request.GET.get('end', None)
            avg = request.GET.get('avg', None)
            change = request.GET.get('change', None)
            # print("=========Date2 ===", type(Date2))
            if Date1 is not None and Date2 is not None and avg == '0' and change == '0':

                queryset = queryset.filter(Open__gt=F('Close')).filter(Date__gte=Date1, Date__lte=Date2)
                print("range and > queryset==========: ",str(queryset.query))
                serializer_class = AnalyzerSerializer(queryset,many=True)
                return Response(serializer_class.data)

            elif Date1 is not None and Date2 is not None and avg == '1' and change == '0':
                queryset1 = Analyzer.objects.values(
                    'Turnover'
                ).filter(Date__gte=Date1, Date__lte=Date2).aggregate(
                    avg_turnover=Avg('Turnover')
                )
                print("average queryset1==========: ", queryset1)
                return Response(queryset1)
            elif Date1 is not None and Date2 is not None and avg == '0' and change == '1':
                    queryset2 = Analyzer.objects.values(
                                'High','Low'
                                ).filter(
                                    Date__gte=Date1, Date__lte=Date2
                                ).aggregate(
                                    avg_change=Avg('High')- Avg('Low')
                                )
                    print("average change diff queryset2==========: ", queryset2)
                    return Response(queryset2)
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