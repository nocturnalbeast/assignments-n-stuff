def is_armstrong(number):
    return sum(map(lambda num:num**len(str(number)) ,map(int, list(str(number))))) == number