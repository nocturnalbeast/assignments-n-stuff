# Woohoo! 10loc!
# Import statement. sys module to recieve the arguments from the command line and textwrap to split the data into chunks of four digits i.e. sixteen bits.
import sys, textwrap

# The franken-code. This is a function that generates a checksum from the given data for the UDP segment.
def ck_gen(src_ip, dst_ip, src_port, dst_port, data):
	# Unifying the source IP and destination IP together, to look like this nnn.nnn.nnn.nnn.nnn.nnn.nnn.nnn; this makes it easier to convert them into the 16-bit segments that we need, avoiding repeating the same process for both the source IP and the destination IP. Then at the end, split it into 8 individual values by splitting at each occurence of '.' .
	all_ele = [int(ele) for ele in '.'.join([src_ip, dst_ip]).split(".")]
	# Unifying all elements that need to be added into the all_ele list. There are three components. The first component is the set of 16-bit segments of the source IP and the destination IP, which is obtained with a list comprehension on the existing all_ele. The second component is all the remaining fields that need to be added, except for the data, and the third element is the integer representation of the 16-bit segments of the data.
	all_ele = [all_ele[i] * 256 + all_ele[i+1] for i in xrange(0,8,2)] + [len(data) + 16, 17, src_port, dst_port] + [int(dat_ele, 16) for dat_ele in textwrap.wrap(data+'0000',4)]
	# Since we got all we need to add in all_ele, go ahead and sum it!
	c_sum = sum(all_ele)
	# Now checking if sum overflows, if yes it will remove it from the sum and add it to the LSBits. All done in int, no conversion needed.
	while c_sum >= 65536: c_sum = (c_sum % 65536) + (c_sum / 65536)
	# Finally return the checksum in the hex format, with necessary padding of '0's added to it. Franken-finished!
	return hex(65535 - c_sum)[2:].zfill(4)

# Getting all the arguments in one line, just cause I can.
src_ip, src_port, dst_ip, dst_port, app_data = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
# Print the final string to be transmitted i.e. the UDP segment.
print hex(src_port)[2:].zfill(4) + hex(dst_port)[2:].zfill(4) + hex(len(app_data)/2 + 8)[2:].zfill(4) + ck_gen(src_ip,dst_ip,src_port,dst_port,app_data) + app_data