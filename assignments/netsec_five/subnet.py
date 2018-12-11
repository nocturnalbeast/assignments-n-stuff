import json, sys, math, textwrap

def conv_to_ip(number):
	return '.'.join([str(int(ele, 2)) for ele in textwrap.wrap(bin(number)[2:].zfill(32), 8)])

def conv_to_num(ip):
	return int(''.join([bin(int(ele))[2:].zfill(8) for ele in ip.split('.')]), 2)

def calc_subnets(needed_hosts, network_addr):
	sub_dict = {str(num):None for num in needed_hosts.keys()}
	consumed = 0
	for subnet in needed_hosts.keys():
		st_ip = conv_to_ip(conv_to_num(network_addr)+consumed)
		en_ip = conv_to_ip(conv_to_num(st_ip)+needed_hosts[subnet]-1)
		temp_dict = {
			"network_addr": st_ip,
			"netmask": conv_to_ip(4294967296 - needed_hosts[subnet]),
			"start_addr": st_ip,
			"end_addr": en_ip,
			"total_host_count": needed_hosts[subnet] - 2
		}
		consumed += needed_hosts[subnet]
		sub_dict[str(subnet)] = temp_dict
	return sub_dict

with open(sys.argv[1]) as in_file:
	data = json.load(in_file)
needed_hosts, network_addr, netmask = data["subnets"], data["network_addr"], data["netmask"]
netmask = ''.join([bin(int(ele))[2:].zfill(8) for ele in netmask.split('.')])
zeroes = netmask.count('0')
needed_hosts = {int(str(key)):2**int(math.ceil(math.log(value+2,2))) for key, value in needed_hosts.items()}
sub_bits = len(bin(len(needed_hosts.keys()))[2:])
if sum(needed_hosts.values()) <= 2**(zeroes - sub_bits):
	answer = {"success":True, "subnets":calc_subnets(needed_hosts, network_addr)}
else:
	answer = {"success":False}
print json.dumps(answer)