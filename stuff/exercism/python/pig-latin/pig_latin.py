def pg_trns(word):
    if word[:2] == 'xr':
        return 'xrayay'  # for some reason
    if word[0] == 'y' and word[1] in 'aeiou':
        word = word[1:] + word[0]
    while word[0] not in 'aeiouy':
        word = word[1:] + word[0]
    if word[-1] == 'q' and word[0] == 'u':
        word = word[1:] + word[0]
    return word + 'ay'

def translate(text):
    trns_lst = [pg_trns(word) for word in text.split()]
    return ' '.join(trns_lst)