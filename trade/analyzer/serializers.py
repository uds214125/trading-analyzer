from rest_framework import serializers
from .models import Analyzer

class AnalyzerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analyzer
        fields = '__all__'
        # fields = ['Date', 'Open','Close' ,'High','Low','Shares_Traded','Turnover']
