/***********************************************************************
* FILENAME : tracker_trie.h
*
* DESCRIPTION :
*       a reTRIEval tree implementation for populating trackers,
*       which includes definition for a single node and the
*       accompanying functions to perform several operaions on the
*       trie structure.
*
* NOTES :
*       The explanation to most of the functionality is described
*       along with the code itself. Refer the comments accompanying
*       the code for the explanation.
*
* AUTHOR : nocturnalbeast
*
***********************************************************************/


/***********************************************************************
* User parameters (specific to tracker entries)
***********************************************************************/

// using all of the printable character range
#define CHAR_RANGE 96
// this is how long a tracker name can be; increase or decrease
// as per requirement
#define TRACKER_SIZE 40


/***********************************************************************
* Basic structure definitions
***********************************************************************/

// the individual trie node, which represents one letter in a string
typedef struct trie_node {

	// the leaf value that contains the count of the tracker, in the
	// event that the node represents the last letter of a tracker entry
	long int leaf_value;
	// an array of pointers to all possible characters in the character
	// range
	struct trie_node *next_char[CHAR_RANGE];

} trie_node;


/***********************************************************************
* Helper functions
***********************************************************************/

// function to generate a new node, and link it to the trie
trie_node* generate_node() {

	// generate a new trie node dynamically
	trie_node* new_node = (trie_node*)malloc(sizeof(trie_node));

	// initalize the leaf value to -1, which means it isn't a leaf node
	new_node->leaf_value = -1;
	// make all the next possible pointers point to NULL
	for (int i = 0; i < CHAR_RANGE; i++)
		new_node->next_char[i] = NULL;

	// return the newly generated node
	return new_node;

}

// function to check if the node in question is a leaf node or not
int check_leaf_node(trie_node* current_node) {

	// not much explanation required, right?
	if (current_node->leaf_value == -1)
		return 0;
	else
		return 1;

}

// function to insert a string into a trie; the name is misleading
void insert_node(trie_node* root, char* insert_str) {

	// set current node as the root node
	trie_node* current_node = root;

	// while the character in the string is not the termination character
	while(*insert_str) {
		// if the next node with the given character does not exist,
		if (current_node->next_char[*insert_str - ' '] == NULL)
			// generate a node for it
			current_node->next_char[*insert_str - ' '] = generate_node();

		// move on to the next node
		current_node = current_node->next_char[*insert_str - ' '];

		// increment the position of the character pointer
		insert_str++;

	}

	// if the leaf node is not designated so, make it so!
	if(!check_leaf_node(current_node))
		current_node->leaf_value = 1;
	// if already done, then increment the value, which is the count
	// of the tracker entry
	else
		current_node->leaf_value++;

}

// function to see if a string is present in the trie; misleading name again
int search_node(trie_node* root, char* search_str) {

	// check if root node is valid
	if(root == NULL)
		return 0;

	// set current node as root node to start with
	trie_node* current_node = root;

	// while the character in the string is not the termination character
	while(*search_str) {

		// move on to the next character
		current_node = current_node->next_char[*search_str - ' '];

		// check if the current node is valid, if not return false
		if(current_node == NULL)
			return 0;

		// increment the position of the character pointer
		search_str++;

	}

	// return the status of the node finally found
	return check_leaf_node(current_node);

}

// function to display all the strings stored in the trie with its accompanying values as well
void display_all_nodes(trie_node* current_node, char op_string[], int level) {

	// check if the current node is a leaf node
	if (check_leaf_node(current_node)) {
		// if yes, terminate the string
		op_string[level] = '\0';
		// print the required stuff :0 using typecast to int to avoid warning
		printf("%s%*ld\n", op_string, (int)(TRACKER_SIZE-strlen(op_string)), current_node->leaf_value);
	}

	// iterate through all the possible pointers to the next characters
	for (int i = 0; i < CHAR_RANGE; i++) {
		// if the next pointer is a valid one
		if (current_node->next_char[i] != NULL) {
			// then add it to the string
			op_string[level] = i + ' ';
			// recursively call the same function, but with incremented value of
			// level, which tells us the number of characters in the output string
			display_all_nodes(current_node->next_char[i], op_string, level + 1);
		}
	}

}

// function to check if a node in the trie contains children or not
int check_children(trie_node* current_node) {

	// not much explanation required, right?
	for(int i = 0; i < CHAR_RANGE; i++) {
		if(current_node->next_char[i])
			return 1;
	}

	return 0;
}

// function to delete a string from a trie; misleading name once again
int delete_node(trie_node* *current_node, char* delete_str) {

	if(*current_node == NULL)
		return 0;

	if(*delete_str) {
		if(*current_node != NULL && (*current_node)->next_char[*delete_str - ' '] != NULL && delete_node(&((*current_node)->next_char[*delete_str - ' ']), delete_str + 1) && (*current_node)->leaf_value == -1) {
			if(!check_children(*current_node)) {
				free(*current_node);
				(*current_node) = NULL;
				return 1;
			}
			else {
				return 0;
			}
		}
	}

	if(*delete_str == '\0' && (*current_node)->leaf_value) {
		if(!check_children(*current_node)) {
			free(*current_node);
			(*current_node) = NULL;
			return 1;
		}
		else {
			(*current_node)->leaf_value = -1;
			return 0;
		}
	}

	return 0;

}