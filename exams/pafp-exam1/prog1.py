def w_print(lst):
    for i in range(len(lst)):
        for j in range(len(lst)-i-1):
            if lst[j] > lst[j+1]:
                temp = lst[j]
                lst[j] = lst[j+1]
                lst[j+1] = temp
    max_pt = len(lst)-1
    min_pt = 0
    while max_pt >= min_pt:
        print lst[max_pt]
        print lst[min_pt]
        max_pt -= 1
        min_pt += 1

lst_in = []
max = input("Enter the maximum range of numbers you'd like to enter:")
print "Enter the numbers:"
for i in xrange(max):
    lst_in.append(input())
w_print(lst_in)