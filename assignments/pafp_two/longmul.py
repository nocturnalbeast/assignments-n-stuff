def longmul(num_a,num_b):
    if len(str(num_a)) + len(str(num_b)) in [2,3]:
        return num_a * num_b
    else:
        a_left,a_right = int(str(num_a)[:len(str(num_a))/2]),int(str(num_a)[(len(str(num_a))/2):])
        b_left,b_right = int(str(num_b)[:len(str(num_b))/2]),int(str(num_b)[(len(str(num_b))/2):])
        return (longmul(a_left,b_left) * 10 ** (len(str(a_right)) + len(str(b_right)))) + (longmul(a_left,b_right) * 10 ** len(str(a_right)) + longmul(a_right,b_left) * 10 ** len(str(b_right))) + (longmul(a_right,b_right))

print "Enter two numbers:"
num1 = input()
num2 = input()
print "The product of the two numbers is " + str(longmul(num1,num2)) + "."