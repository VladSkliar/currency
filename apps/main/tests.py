# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy
from models import Currency, CurrencyValues


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
        currency2 = Currency.objects.create(title='TEST2')
        currency1.values.add(cv1)
        currency1.values.add(cv2)
        currency1.save()

        currency2.values.add(cv1)
        currency2.values.add(cv2)
        currency2.save()
        self.client = Client()

    def test_currencies_responce(self):
        """test status code"""
        self.response = self.client.get(reverse_lazy('currencies'))
        
        self.assertEqual(self.response.status_code, 200)
        json = self.response.json()
        self.assertFalse('TEST-2' in json.keys())
        self.assertTrue('TEST' in json.keys())
        self.assertTrue('TEST2' in json.keys())
        self.assertTrue(self.response['Content-Type'], 'application/json')

    def test_post_data(self):
        self.post_responce = self.client.post(reverse_lazy('currencies'), {'title': 'TEST1'})
        
        self.assertEqual(self.post_responce.status_code, 405)

    def test_one_currency_info(self):
        self.response = self.client.get(reverse_lazy('currency', kwargs={'currency_name':"TEST",}))
        
        self.assertEqual(self.response.status_code, 200)
        json = self.response.json()
        self.assertTrue('TEST-2' in json.keys())
        self.assertFalse('TEST' in json.keys())
        self.assertTrue(self.response['Content-Type'], 'application/json')

    def test_one_currency_info(self):
        self.response = self.client.get(reverse_lazy('currency', kwargs={'currency_name':"TESsaT",}))
        
        self.assertEqual(self.response.status_code, 200)
        json = self.response.json()
        self.assertFalse('TEST-2' in json.keys())
        self.assertTrue('Alert' in json.keys())
        self.assertEqual(u'Wrong currency name', json['Alert'])
        self.assertTrue(self.response['Content-Type'], 'application/json')

    def test_one_currency_info(self):
        self.response = self.client.get(reverse_lazy('currency', kwargs={}))
        
        self.assertEqual(self.response.status_code, 200)
        json = self.response.json()
        self.assertFalse('TEST-2' in json.keys())
        self.assertFalse('TEST' in json.keys())
        self.assertTrue('Alert' in json.keys())
        self.assertEqual(u'No currency name in url pattern', json['Alert'])
        self.assertTrue(self.response['Content-Type'], 'application/json')


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

