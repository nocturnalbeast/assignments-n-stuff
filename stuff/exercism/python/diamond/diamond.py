import string

def make_diamond(letter):
    fst_ltr = list(string.ascii_uppercase)[:ord(letter)-ord('A')+1]
    sze = 2*len(fst_ltr)-1
    lst_dmnd = [gen_line(letter,sze) for letter in fst_ltr]
    return str(lst_dmnd[:len(lst_dmnd)-1] + lst_dmnd[::-1])

def gen_line(letter,ttl_size):
	if letter == 'A':
		return ' ' * (int(ttl_size/2) - 1) + 'A' + ' ' * (int(ttl_size/2) - 1)
	else:
		return letter + ' ' * (ttl_size-2) + letter