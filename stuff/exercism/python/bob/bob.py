import re

def check_question(phrase):
	return len(re.findall("[a-zA-Z0-9]*\?[\s]*$",phrase)) == 1

def check_shout(phrase):
	return (phrase == phrase.upper()) & (len(filter(str.isalpha,phrase)) > 0)

def check_anything(phrase):
	return len(re.sub(r'[\n]*[\r]*[\t]*[\s]*', '', phrase)) == 0


def hey(phrase):
    if check_anything(phrase):
    	return "Fine. Be that way!"
    elif check_question(phrase) & check_shout(phrase):
    	return "Calm down, I know what I'm doing!"
    elif check_question(phrase):
    	return "Sure."
    elif check_shout(phrase):
    	return "Whoa, chill out!"
    else:
    	return "Whatever."