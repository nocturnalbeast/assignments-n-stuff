import re

def is_paired(brkt_str):
	brkt_str = ''.join(re.findall(r'(\{|\}|\[|\]|\(|\))',brkt_str))
	brkt_str = re.sub(r'(\{\}|\[\]|\(\))', '', brkt_str)
	return len(brkt_str) == 0