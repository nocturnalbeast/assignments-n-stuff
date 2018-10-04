trns_dict = {
	2 : ("2 bottles","one"),
	1 : ("1 bottle","it"),
	0 : ("No more bottles",None)
}

def recite(start, take=1):
	sng_lyr_lst = []
	trns_dict.update({num: (str(num) + " bottles","one") for num in xrange(3,100)})
	for i in range(take):
		sng_lyr_lst.append("{0} of beer on the wall, {1} of beer.".format(trns_dict.get(start)[0],trns_dict.get(start)[0].lower()))
		if start > 0:
			sng_lyr_lst.append("Take {0} down and pass it around, {1} of beer on the wall.".format(trns_dict.get(start)[1],trns_dict.get(start-1)[0].lower()))
			start -= 1
		elif start == 0:
			sng_lyr_lst.append("Go to the store and buy some more, 99 bottles of beer on the wall.")
			start = 99
		sng_lyr_lst.append("")
	del sng_lyr_lst[-1]
	return sng_lyr_lst