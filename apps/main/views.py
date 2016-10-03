# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Currency, CurrencyValues

@api_view(['GET',])
def currencies(request):
    currencies = Currency.objects.all()
    response_dict = dict()
    if currencies:
        for currency in currencies:
            response_dict[currency.title] = currency.currency_values
    else:
        response_dict['Alert'] = u'No currencies in db'
    return Response(response_dict)


@api_view(['GET','POST','PUT'])
def currency(request, **kwargs):
    response_dict = dict()
    if request.method == 'POST':
        try:
            currency = Currency.objects.get(title=kwargs['currency_name'])
            response_dict['Alert'] = u'Currency name is register in db'
            response_dict['Detail'] = u"Method 'POST' not allowed. Use 'PUT' method to change"
            return Response(response_dict, status=405)
        except Currency.DoesNotExist:
            data = request.data
            currency = Currency.objects.create(title=kwargs['currency_name'])
            for key, value in data.iteritems():
                currency_value = CurrencyValues.objects.create(title=key,
                                                               value=value)
                currency.values.add(currency_value)
            currency.save()
            response_dict = currency.currency_values
    elif request.method == 'PUT':
        if 'currency_name' in kwargs.keys() and 'curr_value' in kwargs.keys():
            data = request.data
            if 'value' in data.keys():
                try:
                    currency = Currency.objects.get(title=kwargs['currency_name'])
                    currency_value = currency.values.filter(title=kwargs['curr_value']).first()
                    if currency_value:
                        currency_value.value = data['value']
                        currency_value.save()
                    response_dict = currency.currency_values
                except Currency.DoesNotExist:
                    response_dict['Alert'] = u'Wrong currency name'
            else:
                response_dict['Alert'] = u'Wrong put data. Example: {"value":1000}'   
        else:
            response_dict['Alert'] = u'No currency name in url pattern'
    elif request.method == 'GET':
        if kwargs:
            try:
                currency = Currency.objects.get(title=kwargs['currency_name'])
                response_dict = currency.currency_values
            except Currency.DoesNotExist:
                response_dict['Alert'] = u'Wrong currency name'
        else:
            response_dict['Alert'] = u'No currency name in url pattern'
    return Response(response_dict)
