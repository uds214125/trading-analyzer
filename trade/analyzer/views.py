
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
    queryset = User.objects.all()
    serialize_class = AnalyzerSerializer

    def post(self,request):
        if request.method == 'POST':
            serializer = AnalyzerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)