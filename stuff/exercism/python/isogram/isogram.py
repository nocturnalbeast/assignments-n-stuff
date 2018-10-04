def is_isogram(string):
    cln_str = filter(str.isalpha, string.lower())
    return len(set(cln_str)) == len(cln_str)