
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

from django.db.models import F, Avg, Sum, Count, Max, Min, Func
from django.db.models.query import QuerySet
import datetime
# An F() object represents the value of a model field.
# A Q() object, like an F object, encapsulates a SQL expression in a Python object that can be used in database-related operations.
from django.db import models

class AnalyzerList(APIView):
    """
        Get API endpoint which allows get all records, get by filter ( or query)
    """
    # queryset = User.objects.all()
    # serialize_class = AnalyzerSerializer
    # def dispatch(self, *args, **kwargs):
    #     '''
    #         common code here
    #     '''
    #     return super(self).dispatch(*args, **kwargs)
    """
       description : 
       since : 
       author:
    """
    def get(self, request):

        if request.method == 'GET':
            queryset    = Analyzer.objects.all()
            start       = request.GET.get('start', None)
            end         = request.GET.get('end', None)
            avg         = request.GET.get('avg', None)
            change      = request.GET.get('change', None)
            monthwise   = request.GET.get('monthwise', None)
            datewise    = request.GET.get('datewise', None)
            limit       = request.GET.get('limit', None)
            print("=========Trading ========")
            if start is not None and end is not None and avg == '0' and change == '0':

                queryset = queryset.filter(Open__gt=F('Close')).filter(Date__gte=start, Date__lte=end)
                print("range and > queryset==========: ",str(queryset.query))
                serializer_class = AnalyzerSerializer(queryset,many=True)
                return Response(serializer_class.data)

            elif start is not None and end is not None and avg == '1' and change == '0':
                queryset1 = Analyzer.objects.values(
                    'Turnover'
                ).filter(Date__gte=start, Date__lte=end).aggregate(
                    avg_turnover=Avg('Turnover')
                )
                print("average queryset1==========: ", queryset1)
                return Response(queryset1)
            elif start is not None and end is not None and avg == '0' and change == '1':
                # TODO: 
                queryset2 = Analyzer.objects.values(
                                'High','Low'
                                ).filter(
                                    Date__gte=start, Date__lte=end
                                ).aggregate(
                                    avg_change=Avg('High') - Avg('Low')
                                )
                print("average change diff queryset2==========: ", queryset2)
                return Response(queryset2)
                # return Response({'avg_change':''})
            elif monthwise == '1':
                    kwargs = {
                        'open_avg' : Avg('Open'),
                        'close_avg': Avg('Close')
                    }
                    queryset = (Analyzer.objects
                                .annotate(month=Month('Date'))
                                .values('month')
                                .annotate(**kwargs)
                                .order_by())
                    return Response(queryset)
            elif datewise == '1':
                maxData = int(limit) if int(limit) is not None  else 20;
                print(" Max Data To be limit ",maxData)
                metrics = {
                    'avg_turnover': Avg('Turnover'),
                    'maximum_turnover': Max('Turnover'),
                    'minimum_turnover': Min('Turnover'),
                }
                queryset = Analyzer.objects.values(
                    'Date'
                ).annotate(**metrics)[:maxData]
                return Response(queryset)
            else:
                print("Get all record==========:")
                queryset = Analyzer.objects.all()
                serializer_class = AnalyzerSerializer(queryset,many=True)
                return Response(serializer_class.data)
    """
       description : 
       since : 
       author:
    """
    def post(self,request):
        if request.method == 'POST':
            serializer = AnalyzerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()