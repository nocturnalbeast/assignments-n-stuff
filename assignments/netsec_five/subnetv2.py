# Import statements. JSON for handling JSON strings (duh), sys to recieve the command line arguments, math for log operations and textwrap to help with conversion of an integer value to its corresponding IP address.
import json, sys, math, textwrap

# Helper function to convert an integer value to the actual IP address.
def conv_to_ip(number):
	# The one-liner magic. First converts the number into binary representation, then removes the '0b' portion away, then pads it with enough zeroes to make it 32 bits long, then splits it into four parts and then converts the entries of the resulting list into integers and converts those entries into strings, and joins all these entries together, only to be separated by zeroes. Phew.
	return '.'.join([str(int(ele, 2)) for ele in textwrap.wrap(bin(number)[2:].zfill(32), 8)])

# Helper function to convert an IP address into the corresponding integer value.
def conv_to_num(ip):
	# Another one-liner. First splits the IP address into four based on the '.' delimiter, then converts each entry into binary and strips away the '0b' portion away, and pads these converted entries with enough zeroes to make each entry 8 bits long, and then joins all these entries together, which is one 32-bit long binary number which is then converted to an integer. Whew.
	return int(''.join([bin(int(ele))[2:].zfill(8) for ele in ip.split('.')]), 2)

# Function to calculate the subnets and return a dictionary consisting of the data on all the subnets generated.
def calc_subnets(needed_hosts, network_addr):
	# Generating an empty dictionary with all the subnet entries. Their values are set to null.
	sub_dict = {str(num):None for num in needed_hosts.keys()}
	# Declaring a count variable to keep track of the number of IP addresses consumed, and setting it to zero.
	consumed = 0
	# Sorting the needed_hosts dictionary by value (in descending order), and iterating through the sorted list.
	for subnet in sorted(needed_hosts.items(), key=lambda pair: pair[1], reverse=True):
		# Setting the starting IP address of the subnet to the network address plus whatever range of IP addresses has been already consumed.
		st_ip = conv_to_ip(conv_to_num(network_addr)+consumed)
		# Setting the ending IP address of the subnet to the starting network address plus the number of hosts.
		en_ip = conv_to_ip(conv_to_num(st_ip)+subnet[1]-1)
		# Setting up a temporary dictionary to hold all of the required data about each subnet.
		temp_dict = {
			# The network address is the same as the starting address, so assigning it the starting IP address.
			"network_addr": st_ip,
			# Netmask is equal to 001.000.000.000.000 (if such an IP ever existed) minus the range of IPs used in this subnet.
			"netmask": conv_to_ip(4294967296 - subnet[1]),
			# Assigning the starting IP address.
			"start_addr": st_ip,
			# Assigning the ending IP address.
			"end_addr": en_ip,
			# Total host count is the range of IP addresses minus the network address and the broadcast address of the subnet.
			"total_host_count": subnet[1] - 2
		}
		# Adding the range of consumed IP addresses to the consumed variable.
		consumed += subnet[1]
		# Assigning the newly made dictionary to the respective subnet number in the dictionary of subnets.
		sub_dict[str(subnet[0])] = temp_dict
	# Finally, after all the subnets are calculated in the iterator, the dictionary of subnets is returned to the calling function.
	return sub_dict

# Getting the command-line argument and opening the file.
with open(sys.argv[1]) as in_file:
	# Reading the JSON string from the file.
	data = json.load(in_file)
# Reading the data supplied from the JSON string into separate variables.
needed_hosts, network_addr, netmask = data["subnets"], data["network_addr"], data["netmask"]
# Generating the binary representation of the netmask, using the helper function.
netmask = bin(conv_to_num(netmask))[2:]
# Converting the keys in the needed_hosts dictionary into integers (for easier handling), and adding the network address and the broadcast address count into the value and rounding it to the next power of two.
needed_hosts = {int(str(key)):2**int(math.ceil(math.log(value+2,2))) for key, value in needed_hosts.items()}
# Checking if subnetting is possible by checking that the number of hosts needed does not exceed the maximum number of hosts that the network can hold. If it does not exceed, then generate the answer dictionary with the two values, success (being true) and subnets being the dictionary of subnets generated by the calc_subnets function. If it does exceed, then continue to generate an answer that signals the same, with only one value, success set to false.
answer = {"success":True, "subnets":calc_subnets(needed_hosts, network_addr)} if sum(needed_hosts.values()) <= 2**netmask.count('0') else {"success":False}
# Finally printing the output in JSON format.
print json.dumps(answer)