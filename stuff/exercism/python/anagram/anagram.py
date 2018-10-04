from itertools import permutations

def detect_anagrams(word, candidates):
    perms = []
    sel_cands = []
    perm_list = list(permutations(word.lower()))
    for perm in perm_list:
        perms.append(''.join(perm))
    for candidate in candidates:
        if (candidate.lower() in perms) & (word.lower() != candidate.lower()):
            sel_cands.append(candidate)
    return sel_cands