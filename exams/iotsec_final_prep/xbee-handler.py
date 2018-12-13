import serial, os, re

# Prompt to enter the device path / device name.
dev_name = raw_input("Enter the name of the device: ")
# Prompt to get the IP address of the MQTT broker.
broker_ip = raw_input("Enter the IP address of the broker: ")
# Prompt to get the topic name to use whilst publishing the data.
pub_topic = raw_input("Enter the topic name to use: ")
# Initialize the serial device with given default arguments and the device name.
serial_dev = serial.Serial(dev_name, timeout = None, baudrate = 9600, xonoff = False, rtscts = False, dsrdtr = False)
# Initialize an empty string, to recieve the data from the device.
recv_str = ""
# Just an infinite loop to keep receiving data.
while True:
	# Data keeps getting received here.
	try:
		# Receive one character.
		recv_char = serial_dev.read(1)
		# Using regex instead of multiple conditions, logic can still be improved upon.
		if re.search(r'[A-Z]|[a-z]|[0-9]|_', recv_char):
			# Add the character to the string, if the condition is fulfilled.
			recv_str += recv_char
		# If the string contains something, but the next received char does not match the set of filtered characters, then do so.
		if not re.search(r'[A-Z]|[a-z]|[0-9]|_', recv_char) and len(var) > 0:
			# Use os module to spawn a command to execute the mosquitto client to publish the data.
			os.system("mosquitto_pub -h " + broker_ip + " -t " + pub_topic + " -m " + recv_str)
			# Print the data that was transferred.
			print "Data transferred: " + recv_str
			# Reset the string to an empty string.
			recv_str = ""
	# Utilizing a KeyboardInterrupt to end receiving data.
	except KeyboardInterrupt:
		# Break the infinite loop and end the program.
		break
# Finally closing the connection to the serial device upon program termination.
serial_dev.close()