def zeroes_and_ones(lst):
    zero_index = -1
    one_index = len(lst)
    for i in xrange(len(lst)):
        if lst[i] == 0 and i < one_index:
            zero_index += 1
            lst[i] = lst[zero_index]
            lst[zero_index] = 0
        elif lst[i] == 1 and i > zero_index:
            one_index -= 1
            lst[i] = lst[one_index]
            lst[one_index] = 1
    return lst

lst_in = []
max = input("Enter the maximum range of digits you'd like to enter:")
print "Enter the digits:"
for i in xrange(max):
    lst_in.append(input())
print zeroes_and_ones(lst_in)
