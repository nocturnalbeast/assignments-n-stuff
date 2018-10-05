# Import statements for all that's needed; sys for the arguments, socket for creating and managing the server, json for handling the incoming JSON string and converting the final answer to JSON, and threading cause multi-client, duh.
import sys, socket, json, threading
# Yeah, and OrderedDict to retain the final answer's dictionary order.
from collections import OrderedDict

# Class that runs in a separate threads and manages each client. Essentially recieves a client while spawning in a new thread, and manages communication between this program and the client.
class ClientHandler(threading.Thread):
	# Init function to initialise instance variables and init procedures for thread.
 	def __init__(self, c_sock, c_addr):
 		# Start init procedure for each thread.
 		threading.Thread.__init__(self)
 		# Declaring and initialising the instance variables for client address and client connection.
 		# Probably could manage with only the client connection variable.
 		self.c_sock = c_sock
 		self.c_addr = c_addr
 	# Function that actually handles the client
 	def run(self):
 		# Infinite loop. Not much to explain.
	 	# Recieve the JSON string from the client. Now uses makefile, but still slightly unclear. Need to read Python documentation and figure out better ways.
		json_file = self.c_sock.makefile()
 		while True:
 			json_str = json_file.readline()
 			# If the string is the termination character sequence, then end the loop.
 			if json_str == '0\n':
 				break
 			# Or it's assumed to be a valid JSON string, so generate the result from that oh-so-beautiful function below and send the result back to the client.
			res_msg = snl(json_str.strip('\n')) + '\n'
			self.c_sock.send(res_msg)
		# Close all the shiz.
		json_file.close()
 		self.c_sock.close()

# Actual process happens here.
def snl(data):
	# Converting the JSON string to a dictionary.
	dict_game = json.loads(data)
	# Extracting number of players, board size and round data from the above obtained dictionary.
	player_num, board_dim, rounds = dict_game.get('player_count'), dict_game.get('board_dimension'), dict_game.get('die_tosses')
	# Combining the snake entries and ladder entries into a dictionary in the fastest way and normalizing them. This is based on the theory that a snake and a ladder cannot originate from the same place. So instead of having to look up both the dictionaries, this is a much simpler approach as it reduces duplicate code. Plus, it also converts the key values into integer values, for ease of access with actual game processing. Pretty handy.
	dict_lns = {int(key):val for key,val in dict(dict_game.get('ladders'), **dict_game.get('snakes')).items()}
	# Setting values for board minimum (actually the point before the board starts) and the board maximum i.e. the finish point. No actual need for the board minimum, but will be useful if in a twisted case the board begins from some arbitrary number. So yay adaptability!
	board_min, board_max = 0, board_dim ** 2
	# Another beautiful one-liner from yours truly. Essentially what it does is convert all the keys in the rounds data to integer values from its string representations. How it works is by utilizing dict comprehension to traverse through all key-value pairs in rounds and then converting key into int(key) and reassigning the dictionary to the same variable. Also handles sub-dictionary key-value pairs with the help of nested dictionary comprehension. This one-liner also solves a pretty stealthy bug in this approach, and in almost every other approach as well. Figure it out, fellas!
	rounds = {int(key):{int(subkey):subval for subkey,subval in value.items()} for key,value in rounds.items()}
	# Alternate method. Not actually required, but let it be.
	#turn_plyrs = {player+1:[rd_dict[player+1] for rd_dict in rounds.values() if player+1 in rd_dict] for player in xrange(player_num)}
	# Initalising the squares_traversed as a list of lists. Generating it with [] * number makes it reference the same list and that is a PITA. So this utilizes list comprehension to generate lists that do not reference the same element.
	squ_tra = [[] for i in xrange(player_num)]
	# Generating a list for current position for all players to track position of each player as the game goes through each round. It's a list that contains the current position of all players in the game. And as such is initialised to the place before the board starts (recall board_min now?) for all players.
	curr_pos = [board_min] * player_num
	# The mulan schezwan sauce. Not really. Simple nested loop in which the outer loop traverses through keys of the rounds dictionary (iterating through each round, in essence) and the inner loop traverses through the keys of the sub-dictonary which essentially is traversing through each player's die throw.
	for rnd in rounds.keys():
		for player in rounds.get(rnd).keys():
			# Checking to see whether adding the die toss will exceed the board maximum. If not then proceed; but if it does, then nothing is done.
			if (curr_pos[player-1] + rounds.get(rnd).get(player)) <= board_max:
				# Adding the die toss to the current position.
				curr_pos[player-1] += rounds.get(rnd).get(player)
				# Checking if the freshly updated current position is on either a ladder or a snake by checking the combined dictionary. The combined approach saves code and additional checks here.
				if curr_pos[player-1] in dict_lns.keys():
					# If it is a ladder/snake, then append that block to the squares_traversed list for the specified player. The one after climbing the ladder/going down the snake will be handled by the update statement outside this if block.
					squ_tra[player-1].append(curr_pos[player-1])
					# Update the current position of the player with the new position obtained from the combined snakes and ladders dictionary.
					curr_pos[player-1] = dict_lns.get(curr_pos[player-1])
				# Add the current position of the player to the squares_traversed list, even if triggers the ladder/snake condition or not.
				squ_tra[player-1].append(curr_pos[player-1])
	# Phew. We now have all we need, so it's back to one-liners. Now generating final_positions from the squares_traversed list of lists by generating a dictionary (with dictionary comprehension, of course) which sets the key-value pair as the string representation of the player number and the last element of the list corresponding to the respective player in the squares_traversed list.
	fnl_pos = {str(player+1):squ_tra[player][len(squ_tra[player])-1] for player in xrange(len(squ_tra))}
	# Now converting squares_traversed from a list into a dictionary. Did this here and not before because of easier access while writing comprehensions. Don't want to unnecessarily complicate code by using a dict from the start. Plus, generating the previous fnl_pos is easier because this conversion is after it executes and not before it.
	squ_tra = {str(player+1):squ_tra[player] for player in xrange(len(squ_tra))}
	# Generating the game state with a conditional assignment. It'll be 'finished' if any of the players have a final position that is equal to board_max, else 'progress'.
	gme_ste = ('finished' if board_max in fnl_pos.values() else 'progress')
	# Generating the winner list (if more than one winner, if such a case even exists) with a slightly more complicated conditional assignment.
	plr_win = ([player for player in range(1,player_num+1) if fnl_pos.get(str(player)) == board_max] if gme_ste == 'finished' else [None])
	# Converting the list to a single element in case there is only one winner.
	plr_win = (plr_win[0] if len(plr_win) == 1 else plr_win) 
	# Generating answer in JSON format. Utilizing OrderedDict instead of normal dictionary here to preserve order of the key-value pairs, so take that, strict requirements!
	answer = json.dumps(OrderedDict([("winner", plr_win), ("game_state", gme_ste), ("final_positions", fnl_pos), ("squares_traversed", squ_tra)]))
	# At laast. What is love? Baby, don't hurt me, don't hurt me no more.
	return answer

# Finally, code to invoke all this pizazz. Don't think this needs much explanation. Moreover, don't want to. I'm tired of explaining all this.
serv_soc = socket.socket()
serv_soc.bind(('',int(sys.argv[1])))
serv_soc.listen(3)
for i in xrange(3):
	c_sock,c_addr = serv_soc.accept()
	ClientHandler(c_sock,c_addr).start()