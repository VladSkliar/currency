# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy
from models import Currency, CurrencyValues
import json
import csv





class CurrencyModelTest(TestCase):
    def setUp(self):
        cv1 = CurrencyValues.objects.create(title='TEST-1',
                                     value=1.5)
        cv2 = CurrencyValues.objects.create(title='TEST-2',
                                     value=1.8)
        currency = Currency.objects.create(title='TEST',
                                )
        currency.values.add(cv1)
        currency.values.add(cv2)
        currency.save()

    def test_correct_create_currency(self):
        """test for object creation"""
        check_currency = Currency.objects.last()
        self.assertEqual(unicode(check_currency.title), u'TEST')
    
    def test_correct_create_currency_values(self):
        check_currency_values = CurrencyValues.objects.order_by("title").last()
        self.assertEqual(unicode(check_currency_values.title), u'TEST-2')
        self.assertEqual(check_currency_values.value, 1.8)

    def test_correct_create_currency_foreign_key(self):
        check_currency_values = CurrencyValues.objects.last()
        check_currency = Currency.objects.last()

        self.assertEqual(unicode(check_currency.values.first().title), u'TEST-1')
        self.assertEqual(check_currency.values.first().value, 1.5)
        self.assertEqual(check_currency.currency_values, 
                        {'TEST-1':1.5, 'TEST-2':1.8})
        self.assertTrue('TEST-2' in check_currency.currency_values.keys())


class CurrencyViewTest(TestCase):

    def setUp(self):
        cv1 = CurrencyValues.objects.create(title='TEST-1',
                                            value=1.5)
        cv2 = CurrencyValues.objects.create(title='TEST-2',
                                            value=1.8)
        currency1 = Currency.objects.create(title='TEST')
        currency1.values.add(cv1)
        currency1.values.add(cv2)
        currency1.save()
        currency2 = Currency.objects.create(title='TEST2')
        currency2.values.add(cv1)
        currency2.values.add(cv2)
        currency2.save()
        self.client = Client()
        self.get_currencies_response = self.client.get(reverse_lazy('currencies'))
        self.post_response = self.client.post(reverse_lazy('currencies'), {'title': 'TEST1'})
        self.one_currency_response = self.client.get(reverse_lazy('currency', kwargs={'currency_name':"TEST",}))
        self.wrong_currency_response = self.client.get(reverse_lazy('currency', kwargs={'currency_name':"TEddST",}))
        self.empty_currency_response = self.client.get(reverse_lazy('currency', kwargs={}))


    def test_currencies_responce(self):
        """test status code"""
        self.assertEqual(self.get_currencies_response.status_code, 200)
        json = self.get_currencies_response.json()
        self.assertFalse('TEST-2' in json.keys())
        self.assertTrue('TEST' in json.keys())
        self.assertTrue('TEST2' in json.keys())
        
    def test_post_currencies_data(self):        
        self.assertEqual(self.post_response.status_code, 405)

    def test_one_currency_info(self):
        self.assertEqual(self.one_currency_response.status_code, 200)
        json = self.one_currency_response.json()
        self.assertTrue('TEST-2' in json.keys())
        self.assertFalse('TEST' in json.keys())

    def test_wrong_currency_info(self):        
        self.assertEqual(self.wrong_currency_response.status_code, 200)
        json = self.wrong_currency_response.json()
        self.assertFalse('TEST-2' in json.keys())
        self.assertTrue('Alert' in json.keys())
        self.assertEqual(u'Wrong currency name', json['Alert'])

    def test_empty_currency_info(self):
        self.assertEqual(self.empty_currency_response.status_code, 200)
        json = self.empty_currency_response.json()
        self.assertFalse('TEST-2' in json.keys())
        self.assertFalse('TEST' in json.keys())
        self.assertTrue('Alert' in json.keys())
        self.assertEqual(u'No currency name in url pattern', json['Alert'])

    def test_json_format_responce(self):
        self.assertTrue(self.one_currency_response['Content-Type'], 'application/json')
        self.assertTrue(self.post_response['Content-Type'], 'application/json')
        self.assertTrue(self.get_currencies_response['Content-Type'], 'application/json')
        self.assertTrue(self.wrong_currency_response['Content-Type'], 'application/json')
        self.assertTrue(self.empty_currency_response['Content-Type'], 'application/json')


class NoCurrencyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse_lazy('currencies'))

    def test_status(self):
        """test status code"""
        self.assertEqual(self.response.status_code, 200)

    def test_currencies(self):
        """test template render"""
        json = self.response.json()
        self.assertTrue('Alert' in self.response.json().keys())
        self.assertTrue(u'No currencies in db' in self.response.json().values())

    
    def test_json_format(self):
        self.assertTrue(self.response['Content-Type'], 'application/json')

class PostCurrencyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post_response = self.client.post(reverse_lazy('currency', kwargs={'currency_name':"TEST",}), {'Tes':1.1})
        self.seccod_post_responce = self.client.post(reverse_lazy('currency', kwargs={'currency_name':"TEST",}), {'Tes':1.1})
    
    def test_responce(self):
        self.assertEqual(self.post_response.status_code, 201)
        self.assertTrue('Tes' in self.post_response.json().keys())
        

    def test_seccond_responce(self):
        self.assertEqual(self.seccod_post_responce.status_code, 405)
        self.assertTrue('Detail' in self.seccod_post_responce.json().keys())
        self.assertTrue(u"Method 'POST' not allowed. Use 'PUT' method to change" in self.seccod_post_responce.json()["Detail"])

class PutCurrencyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post_response = self.client.post(reverse_lazy('currency', kwargs={'currency_name':"TEST",}), {'Tes':1.1})
        self.put_responce = self.client.put(reverse_lazy('currency', kwargs={'currency_name':"TEST",'curr_value':'Tes'}),
                                            content_type='application/json', data=json.dumps({'value':1.5}))
        self.second_put_responce = self.client.put(reverse_lazy('currency', kwargs={'currency_name':"TEST",'curr_value':'Tesd'}),
                                            content_type='application/json', data=json.dumps({'value':1.5}))

    def test_put_responce(self):
        self.assertEqual(self.put_responce.status_code, 200)
        self.assertTrue('Tes' in self.put_responce.json().keys())
        self.assertEqual(1.5, self.put_responce.json()['Tes'])
        self.assertEqual(self.second_put_responce.status_code, 200)
        self.assertFalse('Tesd' in self.put_responce.json().keys())


class SequenceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse_lazy('sequence'))


    def test_responce(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(self.response['Content-Type'], 'application/json')
        self.assertTrue('Alert' in self.response.json().keys())


    def test_sequence(self):
        names = list()
        currency_dict = dict()
        with open('kurs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if row[0] == '':
                    names = row
                else:
                    i=1
                    currency = {}
                    for value in row[1:]:
                        currency[names[i]] = float(value)
                        i+=1
                    currency_dict[row[0]] = currency
        for currency, currency_value in currency_dict.iteritems():
            self.client.post(reverse_lazy('currency', kwargs={'currency_name':currency,}), currency_value)
        self.response = self.client.get(reverse_lazy('sequence'))
        print self.response.json()
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(self.response['Content-Type'], 'application/json')
        self.assertFalse('Alert' in self.response.json().keys())