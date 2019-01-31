#!/usr/bin/env python2

# using re for regex matching and sys to get command-line arguments.
import re, sys
# using Counter to build the dictionary of counts.
from collections import Counter

# checking if the arguments are provided properly.
if (len(sys.argv) != 2):
	print "\nIncorrect number of arguments passed to the function. Use the script like so: \n\npython2 script.py <logfile>"
	sys.exit(0)

# opening the file and reading all lines into a list.
with open(sys.argv[1], "r") as logfile:
	lines = logfile.readlines()

# initializing lists for the application entries and the tracker occurrences.
app_list = []
tracker_list = []

# the iteration and filtering logic.
# three kinds of lines are needed. One is the header that announces that an application file is being scanned, the second is the number of trackers that are found, and the third is the tracker name listings. These lines are found using regexes and required statements are appended to the respective lists.
for ind in xrange(len(lines)):
	if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}:INFO:====Analysing /var/www/apk/', lines[ind]) and ind < len(lines) -1 :
		if re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}:WARNING:=== Found trackers: ', lines[ind + 1]):
			app_list.append(lines[ind][56:])
			app_list.append(lines[ind + 1][52:])
	if re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}:WARNING: - ', lines[ind]):
		tracker_list.append(lines[ind][35:])

# using Counter to build the count of occurrences of each tracker, very easy and efficient method.
# this part is pretty simple, take the list of trackers previously made, then use Counter method to build a dictionary of the number of occurrences of each tracker, and then a simple iterative print block to pretty print the data.
count = dict(Counter(tracker_list))
print "\n" + "Tracker Name" + " "*28 + "Number of occurrences" + "\n"
for ele in sorted(count.items(), key = lambda ele: ele[1], reverse = True):
	print ele[0].strip("\n") + " " + "-"*(40-len(ele[0])) + str(ele[1])

# the other part; building the list of apps with their number of trackers.
# making use of a list comprehension to split the lines into tuples of three, in which each tuple contains the singature of the package, the package name and the number of trackers found in the application, then sorting it in the reverse order with respect to the number of trackers and then a simple iterative print block to pretty print the data of the top 100 applications.
entries = [(app_list[ind].strip("\n").split("_")[0] ,app_list[ind].strip("\n").split("_")[1], int(app_list[ind+1].strip("\n"))) for ind in xrange(0, len(app_list), 2)]
entries.sort(key = lambda ele: ele[2], reverse = True)
print "\n" + "Package Signature" + " "*18 +"Application Name" + " "*34 + "Number of trackers" + "\n"
for ind in xrange(min(len(entries), 100)):
	print entries[ind][0] + "   " + entries[ind][1] + "-"*(50-len(entries[ind][1])) + str(entries[ind][2])