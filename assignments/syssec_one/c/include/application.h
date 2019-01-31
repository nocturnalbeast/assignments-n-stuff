/***********************************************************************
* FILENAME : application.h
*
* DESCRIPTION :
*       The data structure used to represent an application, storing
*       its constituent data, alongside helper functions to perform
*       varoius operations on the objects of the structure.
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
* User parameters (specific to application entries)
***********************************************************************/

// the maximum size that an application name can be
#define APPLICATION_SIZE 65
// the size of the application signature
#define SIGNATURE_SIZE 32
// sorting order; 0 -> descending and 1 -> ascending
#define SORTING_ORDER 0


/***********************************************************************
* Basic structure definitions
***********************************************************************/

// the individual application node/object
typedef struct application_node {

	// the application name
	char app_name[APPLICATION_SIZE];
	// the signature of the application package provided
	char app_signature[SIGNATURE_SIZE];
	// the number of trackers detected
	int count_trackers;

} application_node;


/***********************************************************************
* Helper functions
***********************************************************************/

// function to generate an application object; not really used in
// the code though
application_node* generate_app_node(char* app_name, char* app_signature, int count_trackers) {

	// generate a new node dynamically
	application_node* new_node = (application_node*)malloc(sizeof(application_node));

	// assign all the arguments passed into the data members of the
	// struct variable
	strcpy(new_node->app_name, app_name);
	strcpy(new_node->app_signature, app_signature);
	new_node->count_trackers = count_trackers;

	// return the newly created node
	return new_node;

}

// function to update the exsisting application object with values
// given as arguments into the function
void update_app_node(application_node* node, char* app_name, char* app_signature, int count_trackers) {

	// assign all the arguments passed into the data members of the
	// struct variable
	strcpy(node->app_name, app_name);
	strcpy(node->app_signature, app_signature);
	node->count_trackers = count_trackers;

}

// function to increase the size of the application object list
// it's just a wrapper for realloc, really
application_node* resize_list(application_node* app_list, int size) {

	// just resize the list with realloc, assign to a struct pointer
	application_node* list_resized = (application_node*)realloc(app_list, size * sizeof(application_node));
	// then return that pointer
	return list_resized;

}

// comparator function used for qsort function
int compare(const void *one, const void *two) {

	// typecasting the pointers recieved as arguments into application
	// node pointers
	const application_node *ptr_one = (const struct application_node*)one;
	const application_node *ptr_two = (const struct application_node*)two;

	// decide compare order based on the sorting order and then compare
	// as given
	if ( !SORTING_ORDER )
		return ( ptr_two->count_trackers - ptr_one->count_trackers );
	else
		return ( ptr_one->count_trackers - ptr_two->count_trackers );

}