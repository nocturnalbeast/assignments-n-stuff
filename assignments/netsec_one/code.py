# The modules that this program requires
import re, json, sys, socket

# Function to format the recieved string
def format(string):
    # Using re.split to split all elements, re is faster than string
    ele_lst = re.split(r'\|\|',string)
    # Extracting number of players and number of rounds from list of elements, list now contains only the data on rounds
    num_players, num_rounds, ele_lst = int(ele_lst[0]), int(ele_lst[1]), ele_lst[2:]
    # Find the position of all zero elements in the list of elements
    zer_arr = [i for i, e in enumerate(ele_lst) if e == '0']
    # List comprehension to generate a list of elements out of the given zero positions by iterating through the list of positions of zero made just before
    rounds_data = [ele_lst[:zer_arr[i]] if i == 0 else ele_lst[zer_arr[i-1]+1:zer_arr[i]] for i in xrange(len(zer_arr))]
    # The masterpiece - dict comprehension which nests another dict comprehension which hosts multiple string splicing and splitting.
    # Explanation: By the end of the last statement, rounds_data is now a list of lists, in which each sublist is like so : ['1', '1:2,0,S,W', '3:0,1,S']
    # Now the outer dict comprehension handles element as a key-value pair which cycles through each sublist, which takes first element as key and remaining elements as a list which is the value of the key-value pair.
    # The inner dict comprehension handles the rest of the sublist by splitting each key and value with the : and , delimiter and makes it a key-value pair with the help of some magic splitting and splicing ;)
    rounds_data = {int(element[0]):{int(string.split(':')[0]):string.split(':')[1].split(',') for string in element[1:]} for element in rounds_data}
    # Return these to next function
    return num_players,num_rounds,rounds_data

# Helper function to compute score
def find_score(card_lst):
    # Dictionary approach to lookup scores
    dict_card_trns = { 'S' : 20, 'T' : 20, 'R' : 20, 'W' : 50, 'F' : 50 }
    # Generating a list with list comprehension with all the corresponding scores from the cards, then passing it to the sum function and returning that value. Pretty nifty. You can never get enough of one-liners.
    return sum([dict_card_trns.get(element) if element in dict_card_trns.keys() else int(element) for element in card_lst])

# Finally the function that processes the game
def proc_game(num_players,num_rounds,rounds_data):
    # Generate list of round winners with dictionary comprehension where the key becomes stringified round number and the value is list of the set difference of all the players and the players whose data is shown in the round
    round_winners = {str(rnd):list(set(range(1,num_players+1)) - set(rounds_data.get(rnd).keys())) for rnd in rounds_data.keys()}
    # Normalise the key-value pair by modifying the value list to be a single element if the list only contains a single element
    round_winners = {rnd:(winner[0] if len(winner) == 1 else winner) for rnd,winner in round_winners.items()}
    # Generate a list of scores of all rounds with a list comprehension. Cool.
    round_score = [find_score([card for hand in rounds_data.get(rnd).values() for card in hand]) for rnd in rounds_data.keys()]
    # Initalise the dictionary for scores with a simple dictionary comprehension
    scores = {str(player):0 for player in xrange(1,num_players+1)}
    # Under work. not too shabby, but still needs work. Can't manage with a dict comprehension, it seems. Can't handle multiple round winners too.
    for ind_rs in xrange(len(round_score)):
        scores.update({str(round_winners.get(str(ind_rs+1))):scores.get(str(round_winners.get(str(ind_rs+1)))) + round_score[ind_rs]})
    # One-line magic for the winner!
    overall_winner = [player for player in range(1,num_players+1) if scores.get(str(player)) == max(scores.values())]
    # Making list into a single element if list contains only one element
    overall_winner = (overall_winner[0] if len(overall_winner) == 1 else overall_winner)
    # Generating answer in JSON format.
    answer = json.dumps({
        "round_winners" : round_winners,
        "overall_winner" : overall_winner,
        "scores" : scores,
    })
    # RETURN EEEET!!!!!!! Phew.
    return answer


# Run-of-the-mill driver code.
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((sys.argv[1], int(sys.argv[2])))
string = client_sock.recv(8192)
while string != "0\n":
    fmtd_tple = format(string)
    send_str = proc_game(fmtd_tple[0],fmtd_tple[1],fmtd_tple[2])
    client_sock.send(send_str)
    string = client_sock.recv(8192)
client_sock.close()