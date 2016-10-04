
def count_sequences(g_currency, result_dict, n):
    if len(result_dict)==0:
        for key,value in g_currency.iteritems():
            name = key
            for k,v in value.iteritems():
                if v!=1:
                    name = name + ',' + k
                    result_dict[name] = float(v)
                name = key
        n -= 2
        count_sequences(g_currency, result_dict, n)
    else:
        if n > 1:
            check_dict = result_dict.copy()
            for k,v in check_dict.iteritems():
                key = k.split(',')[-1]
                if key != k.split(',')[0]:
                    value = g_currency[key]
                    for iter_key,iter_value in value.iteritems():
                        if key!=iter_key:
                            new_name = k + ',' + iter_key
                            new_value = v*iter_value
                            result_dict[new_name] = new_value
                if len(k.split(','))<3:
                    result_dict.pop(k, False)
            n -= 1
            count_sequences(g_currency, result_dict, n)
        elif n == 1:
            check_dict = result_dict.copy()
            for k,v in check_dict.iteritems():
                key = k.split(',')[-1]
                if key != k.split(',')[0]:
                    value = g_currency[key]

                    for iter_key,iter_value in value.iteritems():
                        if key!=iter_key:
                            new_name = k + ',' + iter_key
                            new_value = v*iter_value
                            result_dict[new_name] = new_value
                if len(k.split(','))<3:
                    result_dict.pop(k, False)
            n -= 1
            count_sequences(g_currency, result_dict, n)
        elif n == 0:
            check_dict = result_dict.copy()
            for k,v in check_dict.iteritems():
                if k.split(',')[0] != k.split(',')[-1]:
                    result_dict.pop(k, False)