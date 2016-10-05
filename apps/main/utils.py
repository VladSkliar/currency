
def count_sequences(g_currency, result_dict, n):
    if len(result_dict) == 0:
        '''
        If result dict is empty add start data in result dict
        Example of g_currency - matrix of currencies:
        {
            "USD": {
                "USD": 1.0,
                "EUR": 0.9,
                "RUB": 65.0,
                "CNY": 6.0
            },
            "EUR": {
                "USD": 1.1,
                "EUR": 1.0,
                "RUB": 70.0,
                "CNY": 6.5
            },
            "RUB": {
                "USD": 0.02,
                "EUR": 0.01,
                "RUB": 1.0,
                "CNY": 0.08
            },
            "CNY": {
                "USD": 0.17,
                "EUR": 0.16,
                "RUB": 10.75,
                "CNY": 1.0
            }
        }
        n - step count for build sequence
        '''
        for key, value in g_currency.iteritems():
            name = key
            for k, v in value.iteritems():
                '''
                If currency value == 1 - pass
                '''
                if v != 1:
                    name = name + ',' + k
                    result_dict[name] = float(v)
                name = key
        '''
        In result dict 2 step counting
        '''
        n -= 2
        '''
        Recursively call function for filling result dict
        '''
        count_sequences(g_currency, result_dict, n)
    else:
        if n > 1:
            '''
            If count of step greter than 1 add new sequnce in  result dict
            '''
            check_dict = result_dict.copy()
            for k, v in check_dict.iteritems():
                key = k.split(',')[-1]
                if key != k.split(',')[0]:
                    value = g_currency[key]
                    for iter_key, iter_value in value.iteritems():
                        if key != iter_key:
                            new_name = k + ',' + iter_key
                            new_value = v*iter_value
                            result_dict[new_name] = new_value
                if len(k.split(',')) < 3:
                    result_dict.pop(k, False)
            n -= 1
            count_sequences(g_currency, result_dict, n)
        elif n == 0:
            check_dict = result_dict.copy()
            for k, v in check_dict.iteritems():
                if k.split(',')[0] != k.split(',')[-1]:
                    result_dict.pop(k, False)
        '''            
        elif n == 1:
            check_dict = result_dict.copy()
            for k, v in check_dict.iteritems():
                key = k.split(',')[-1]
                if key != k.split(',')[0]:
                    value = g_currency[key]
                    for iter_key, iter_value in value.iteritems():
                        if key != iter_key:
                            new_name = k + ',' + iter_key
                            new_value = v*iter_value
                            result_dict[new_name] = new_value
                if len(k.split(',')) < 3:
                    result_dict.pop(k, False)
            n -= 1
            count_sequences(g_currency, result_dict, n)
        '''
