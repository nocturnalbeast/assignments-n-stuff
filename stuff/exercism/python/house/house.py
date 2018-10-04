lst_rhyme = [
	['lay in ', 'the house that Jack built.'],
	['ate ', 'the malt '],
	['killed ', 'the rat '],
	['worried ', 'the cat '],
	['tossed ', 'the dog '],
	['milked ', 'the cow with the crumpled horn '],
	['kissed ', 'the maiden all forlorn '],
	['married ', 'the man all tattered and torn '],
	['woke ', 'the priest all shaven and shorn '],
	['kept ', 'the rooster that crowed in the morn '],
	['belonged to ', 'the farmer sowing his corn '],
	['None', 'the horse and the hound and the horn ']
]

def recite(start_verse, end_verse):
	lst_lines = []
	for j in xrange(end_verse-start_verse+1):
		line = ''
		for i in xrange(start_verse+j-1):
			line = "that " + lst_rhyme[i][0] + lst_rhyme[i][1] + line
		line = "This is " + lst_rhyme[start_verse+j-1][1] + line
		lst_lines.append(line)
	return lst_lines
