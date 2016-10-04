# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Currency, CurrencyValues
from utils import count_sequences


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
            return Response(response_dict, status=201)
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

@api_view(['GET',])
def sequence(request):
    currencies = Currency.objects.all()
    response_dict = dict()
    if currencies:
        currency_dict = dict()
        for currency in currencies:
            currency_dict[currency.title] = currency.currency_values
        sequences_dict = dict()
        count_sequences(currency_dict, sequences_dict, len(currency_dict))
        response_dict["profit_percent"] = 1.01
        response_dict["sequence"] = []
        for key, value in sequences_dict.iteritems():
            if value == response_dict["profit_percent"]:
                if len(response_dict["sequence"])>0:
                    if len(key.split(','))<len(response_dict["sequence"]):
                        response_dict["sequence"] = key.split(',')
                        response_dict["profit_percent"] = value
                else:
                    response_dict["sequence"] = key.split(',')
                    response_dict["profit_percent"] = value
            elif value > response_dict["profit_percent"]:
                response_dict["sequence"] = key.split(',')
                response_dict["profit_percent"] = value
            else:
                response_dict["profit_percent"] = 1.01
                response_dict["sequence"] = 'no risk-free opportunities exist yielding over 1.00% profit exist'
    else:
        response_dict['Alert'] = u'No currencies in db'
    return Response(response_dict)