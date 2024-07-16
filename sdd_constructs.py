import math


def binary_search(pattern: int, int_array: "str|list|tuple", min_pos, max_pos):

    m = math.floor(((min_pos+max_pos)/2))
    if(int_array[m] == pattern):
        return m
    elif(int_array[m] < pattern):
        min_pos = m
        binary_search(pattern, int_array, min_pos, max_pos)
    elif(int_array[m] > pattern):
        max_pos = m
        binary_search(pattern, int_array, min_pos, max_pos)
    return -1


def bubble_sort(_array: "list[int]|tuple[int]", stop=0):
    backer = list(_array)
    min_ = _array[stop]
    min_pos = stop
    if(stop == len(_array)-1):
        return backer

    for i in range(len(_array)-1, stop, -1):
        if(min_ > _array[i]):
            min_ = _array[i]
            min_pos = i

    for i in range(len(_array)-1, stop, -1):
        if(i <= min_pos):
            backer[i] = backer[i-1]

    backer[stop] = _array[min_pos]

    return bubble_sort(backer, stop+1)
