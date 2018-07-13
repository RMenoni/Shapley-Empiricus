import v_value

def subseq(seq):
    n = len(seq)
    for i in range(1, 2**n):
        b = format(i, f'0{n}b')
        s = []
        for j in range(len(b)):
            if int(b[-j-1]) == 1:
                s.append(seq[j])
        s.sort()
        yield ','.join(s)

"""
Deprecado; Versoes novas em shapley_value.pyx

def v_function(A, C_values):
    worth_of_A = 0
    for subset in subseq(A.split(',')):
        subset.sort()
        subset = ','.join(subset)
        if subset in C_values.keys():
            worth_of_A += C_values[subset]
    return worth_of_A


def get_v_values(channels, C_values):
    import os.path
    import pickle
    filename = 'v_values.pickle'
    if os.path.isfile(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    v_values = {}
    count = 0
    for A in subseq(channels):
        count += 1
        A = ','.join(A)
        print(f'{count}: {A}\r', end='')
        v_values[A] = v_function(A, C_values)
    print(f'\n{v_values}')
    with open(filename, 'wb') as file:
        pickle.dump(v_values, file)
    return v_values
"""

def shapley(channels, v_values):
    from collections import defaultdict
    from math import factorial
    n = len(channels)
    res = defaultdict(float)
    count = 0
    for channel in channels:
        count += 1
        print(f'channel {count} of {n}')
        for A in v_values.keys():
            A_arr = A.split(',')
            if channel not in A_arr:
                cardinal_A = len(A_arr)
                A_with_channel = A_arr
                A_with_channel.append(channel)
                A_with_channel = ','.join(sorted(A_with_channel))
                res[channel] += (v_values[A_with_channel] - v_values[A])*(factorial(cardinal_A)*factorial(n-cardinal_A-1)/factorial(n))
        res[channel] += v_values[channel] / n
    return res


def main():
    import pandas as pd
    df = pd.read_csv('shapley_source.csv')
    C_values = df.set_index('copy_list').to_dict()['conversions']
    channels = sorted([c for c in C_values.keys() if ',' not in c])
    print(sum(C_values.values()))
    v_values = v_value.get_v_values(channels, C_values)
    s = shapley(channels, v_values)
    for c in channels:
        assert(s[c] >= C_values[c])
    sorted_res = sorted(s.items(), key=lambda kv: kv[1])
    from pprint import pprint
    pprint(sorted_res)
    print(sum(s.values()))


main()
