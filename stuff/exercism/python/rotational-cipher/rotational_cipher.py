from string import maketrans

def rotate(text, key):
    nonrot_key = 'abcdefghijklmnopqrstuvwxyz'
    rot_key = nonrot_key[key:] + nonrot_key[:key]
    rot_table = maketrans(nonrot_key,rot_key)
    rot_table_upper = maketrans(nonrot_key.upper(),rot_key.upper())
    return text.translate(rot_table).translate(rot_table_upper)
