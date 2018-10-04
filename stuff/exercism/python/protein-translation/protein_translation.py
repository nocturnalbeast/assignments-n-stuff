dict_nme = {
	'AUG': "Methionine",
	'UUU': "Phenylalanine",
	'UUC': "Phenylalanine",
	'UUA': "Leucine",
	'UUG': "Leucine",
	'UCU': "Serine",
	'UCC': "Serine",
	'UCA': "Serine",
	'UCG': "Serine",
	'UAU': "Tyrosine",
	'UAC': "Tyrosine",
	'UGU': "Cysteine",
	'UGC': "Cysteine",
	'UGG': "Tryptophan",
	'UAA': "STOP",
	'UAG': "STOP",
	'UGA': "STOP"
}

def proteins(strand):
	lst_prot = [dict_nme.get(strand[i:i+3]) for i in range(0,len(strand),3)]
	if "STOP" in lst_prot:
		return lst_prot[:lst_prot.index("STOP")]
	else:
		return lst_prot