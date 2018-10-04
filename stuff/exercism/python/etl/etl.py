def transform(legacy_data):
	dict_new = {}
	for score in legacy_data:
		for letter in legacy_data.get(score):
			dict_new[letter.lower()] = score
	return dict_new