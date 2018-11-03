def z_n_o(lst):
    zero_index = -1
    one_index = len(lst)
    arr = [None] * len(lst)
    for i in lst:
        if i == 0:
            zero_index += 1
            arr[zero_index] = 0
        elif i == 1:
            one_index -= 1
            arr[one_index] = 1
    return arr

lst_in = []
max = input("Enter the maximum range of digits you'd like to enter:")
print "Enter the digits:"
for i in xrange(max):
    lst_in.append(input())
print z_n_o(lst_in)
