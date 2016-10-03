from models import Currency
from rest_framework import routers, serializers, viewsets

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = ('url', 'title', 'currency_values')