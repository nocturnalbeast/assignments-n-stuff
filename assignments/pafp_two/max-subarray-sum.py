def max_cross_sum(list_ele, l, m, r):
    left_sum = 0
    right_sum = 0
    sum = 0
    for i in range(l, m+1, -1):
        sum += list_ele[i]
        if sum > left_sum:
            left_sum = sum
    sum = 0
    for i in range(m, r+1, 1):
        sum += list_ele[i]
        if sum > right_sum:
            right_sum = sum
    return left_sum + right_sum

def max_subarray_sum(list_ele, l, r):
    if l == r:
        return list_ele[l]
    m = (l + r) / 2
    return max(max_subarray_sum(list_ele, l, m),max_subarray_sum(list_ele, m+1, r),max_cross_sum(list_ele, l, m, r))

list_ele = []
size = input("How many elements do you want in your list? ")
for ind in xrange(size):
    ele = input("Enter an element: ")
    list_ele.append(ele)
mxsasm = max_subarray_sum(list_ele, 0, size-1)
print "The maximum subarray sum is " + str(mxsasm) + "."