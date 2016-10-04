# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models import Currency, CurrencyValues
from utils import count_sequences
import csv


@api_view(['GET'])
def currencies(request):
    '''
    Get all Currency in DB and responce them
    if DB hasn`t have currency response alert
    '''
    currencies = Currency.objects.all()
    response_dict = dict()
    if currencies:
        for currency in currencies:
            response_dict[currency.title] = currency.currency_values
    else:
        response_dict['Alert'] = u'No currencies in db'
    return Response(response_dict)


@api_view(['GET', 'POST', 'PUT'])
def currency(request, **kwargs):
    response_dict = dict()
    if request.method == 'POST':
        '''
        Try find that currency in DB 
        if currency in DB return 405 status code
        if no currency in DB create  and retunr 201 status code
        '''
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
        '''
        Validate request data
        '''
        if 'currency_name' in kwargs.keys() and 'curr_value' in kwargs.keys():
            data = request.data
            if 'value' in data.keys():
                '''
                Try find currency in DB and put new currency value
                if currency doesn`t find return alert
                if currency value doesn`t 
                find return condition of currency in DB
                '''
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


@api_view(['GET'])
def sequence(request):
    currencies = Currency.objects.all()
    response_dict = dict()
    if currencies:
        currency_dict = dict()
        '''
        Create currency dictionary
        '''
        for currency in currencies:
            currency_dict[currency.title] = currency.currency_values
        sequences_dict = dict()
        '''
        Create all sequences in currency dictionary
        '''
        count_sequences(currency_dict, sequences_dict, len(currency_dict))
        response_dict["profit_percent"] = 1.01
        response_dict["sequence"] = 'no risk-free opportunities exist yielding over 1.00% profit exist'
        '''
        Select the optional sequence in sequences dict
        '''
        for key, value in sequences_dict.iteritems():
            if value == response_dict["profit_percent"]:
                if len(response_dict["sequence"]) > 0:
                    if len(key.split(',')) < len(response_dict["sequence"]):
                        response_dict["sequence"] = key.split(',')
                        response_dict["profit_percent"] = value
                else:
                    response_dict["sequence"] = key.split(',')
                    response_dict["profit_percent"] = value
            elif value > response_dict["profit_percent"]:
                print value, key
                response_dict["sequence"] = key.split(',')
                response_dict["profit_percent"] = value
                print response_dict
    else:
        response_dict['Alert'] = u'No currencies in db'
    return Response(response_dict)


def index(request):
    context = {}
    if request.method == 'POST':
        if request.FILES:
            if request.FILES['file'].name.split('.')[-1] == 'csv':
                destination = open(settings.MEDIA_ROOT + '/' + request.FILES['file'].name, 'wb+')
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
                destination.close()
                names = list()
                currency_dict = dict()
                with open(settings.MEDIA_ROOT + '/' + request.FILES['file'].name, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile)
                    for row in spamreader:
                        if row[0] == '':
                            names = row
                        else:
                            i = 1
                            currency = {}
                            for value in row[1:]:
                                currency[names[i]] = float(value)
                                i += 1
                            currency_dict[row[0]] = currency
                currencies = Currency.objects.all()
                for obj in currencies:
                    for value in obj.values.all():
                        obj.values.remove(value)
                    obj.delete()
                for currency_title, currency_value in currency_dict.iteritems():
                    currency = Currency.objects.create(title=currency_title)
                    for key, value in currency_value.iteritems():
                        c_value = CurrencyValues.objects.create(title=key,
                                                                value=value)
                        currency.values.add(c_value)
                    currency.save()
                import os
                os.remove(settings.MEDIA_ROOT + '/' + request.FILES['file'].name)
            else:
                context['message'] = 'Wrong file format'
    currencies = Currency.objects.all()
    if currencies:
        context['currency'] = True
    return render(request, 'index.html', context=context)
