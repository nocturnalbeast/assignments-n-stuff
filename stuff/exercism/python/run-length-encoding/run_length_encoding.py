import re

def decode(string):
    nrml_str = re.sub(r'([a-zA-Z ])(?=[a-zA-Z ])',r'\1.1',string).replace(".","")
    nrml_str = re.sub(r'(^[a-zA-Z ])',r'1\1',nrml_str)
    exp_list = re.findall(r'([0-9]+)([a-zA-Z ])',nrml_str)
    dec_str = ''
    for entry in exp_list:
    	dec_str += entry[1] * int(entry[0])
    return dec_str

def encode(string):
    rle_lst = re.findall(r"(([a-zA-Z ])\2*)", string)
    rle_str = ''
    for entry in rle_lst:
    	if entry[0] == entry[1]:
    		rle_str += entry[0]
    	else:
    		rle_str += str(len(entry[0]))
    		rle_str += entry[1]
    return rle_str