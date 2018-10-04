import re
from collections import Counter

def word_count(phrase):
	return Counter(re.findall(r"[0-9]+|[a-z]+[']?[a-z]+", phrase.lower()))