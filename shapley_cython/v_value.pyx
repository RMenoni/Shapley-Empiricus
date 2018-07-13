def subseq(seq):
    cdef int n = len(seq)
    cdef int i
    for i in range(1, 2**n):
        b = format(i, f'0{n}b')
        list s = []
        cdef int j
        for j in range(len(b)):
            if int(b[-j-1]) == 1:
                s.append(seq[j])
        s.sort()
        yield ','.join(s)


cpdef int v_function(str A, dict C_values):
    """
    Computes worth of one coalition of channels
    :param A: a coalition of channels
    :param C_values: dict with conversion # of each set of channels
    :return: worth of A
    """
    cdef int worth_of_A = 0
    cdef str subset
    for subset in subseq(A.split(',')):
        if subset in C_values.keys():
            worth_of_A += C_values[subset]
    return worth_of_A


cpdef dict get_v_values(list channels, dict C_values):
    import os.path
    import pickle
    cdef str filename = 'v_values.pickle'
    if os.path.isfile(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    cdef dict v_values = {}
    cdef int count = 0
    cdef str A
    for A in subseq(channels):
        count += 1
        print(f'{count}: {A}\r')
        v_values[A] = v_function(A, C_values)
    print(f'\n{v_values}')
    with open(filename, 'wb') as file:
        pickle.dump(v_values, file)
    return v_values
