/***********************************************************************
* FILENAME : parser.c
*
* DESCRIPTION :
*       A parser built to generate ranked lists of applications
*       and it's tracker counts by parsing given log files.
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
* Headers
***********************************************************************/

// include standard header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>

// include custom header files; refer respective files for further explanation
#include "include/tracker_trie.h"
#include "include/application.h"


/***********************************************************************
* User parameters
***********************************************************************/

// maximum size of a line in the log file
#define LINE_SIZE 400
// increment step for increasing the length of the list
#define REALLOC_STEP 4
// number of applications to display in the result
#define APPS_TO_DISPLAY 100
// option to trim the file extension, if needed; 1 -> true and 0 -> false
#define TRIM_EXTENSION 1


/***********************************************************************
* Accompanying functions
***********************************************************************/

// the function that reads the logfile and parses it, to build the required lists
int parser(FILE *logfile, trie_node* root_node, application_node* *app_list) {

	// regexes used to match three kinds of lines; the start of one application,
	// the accompanying line containing the count and the lines denoting each
	// tracker entry
	regex_t analysis_start_r, tracker_num_r, tracker_entry_r, app_entry_r;
	// return statuses for regex compilation
	int analysis_start_s, tracker_num_s, tracker_entry_s, app_entry_s;
	// regex match structure for the app entry
	regmatch_t app_entry_m;
	// count of applications found
	long int num_apps = 0;

	// compiling the regexes
	analysis_start_s = regcomp(&analysis_start_r, "^[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2} [[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2},[[:digit:]]{3}:INFO:====Analysing /var/www/apk/", REG_EXTENDED);
	tracker_num_s = regcomp(&tracker_num_r, "^[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2} [[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2},[[:digit:]]{3}:WARNING:=== Found trackers: ", REG_EXTENDED);
	tracker_entry_s = regcomp(&tracker_entry_r, "^[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2} [[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2},[[:digit:]]{3}:WARNING: - ", REG_EXTENDED);
	app_entry_s = regcomp(&app_entry_r, "[0-9a-f]{32}_.*", REG_EXTENDED | REG_ICASE);

	// checking for successful compilation of the regex variables
	if (analysis_start_s || tracker_num_s || tracker_entry_s || app_entry_s) {
		// if not, issue error message
		printf("Error in compiling regular expressions. The program will now exit.\n");
		// and exit returning error code
		exit(1);
	}

	// the main parsing block
	// first checks if the logfile has been opened correctly
	if (logfile != NULL) {

		// declaring character arrays to act as buffers for file read ops
		char ln_one[LINE_SIZE], ln_two[LINE_SIZE], ln_three[LINE_SIZE];
		// dummy pointer for the strtol function used
		char *dummy;

		// while the end of the file has not been reached:
		while (fgets(ln_one, LINE_SIZE, logfile) != NULL) {
			// if the line read matches the regex condition representing
			// the start of the application:
			if (!regexec(&analysis_start_r, ln_one, 0, NULL, 0)) {
				// read the next line, if the end of the file has not been reached:
				if (fgets(ln_two, LINE_SIZE, logfile) != NULL) {
					// if the line read matches the regex condition representing the line
					// that accompanies the line that represents the start of the
					// application:
					if (!regexec( &tracker_num_r, ln_two, 0, NULL, 0)) {

						// trim the last space and newline character from the first line
						// also handles trimming the file extension
						ln_one[strlen(ln_one)-2-(TRIM_EXTENSION*4)] = '\0';
						// trim the newline character from the second line
						ln_two[strlen(ln_two)-1] = '\0';

						// extract the actual app entry from the first string
						if (!regexec(&app_entry_r, ln_one, 1, &app_entry_m, 0))
							snprintf(ln_one, LINE_SIZE, "%.*s", (int)(app_entry_m.rm_eo - app_entry_m.rm_so), ln_one + app_entry_m.rm_so);

						// extract the package signature into one buffer
						memmove(ln_three, ln_one, SIGNATURE_SIZE);
						// fix the ending on the signature string
						ln_three[SIGNATURE_SIZE] = '\0';
						// extract the package name into another buffer
						memmove(ln_one, ln_one + SIGNATURE_SIZE + 1, sizeof(ln_one) - (SIGNATURE_SIZE + 1));
						// extract the tracker count into yet another buffer
						memmove(ln_two, ln_two + 52, sizeof(ln_two) - 52);

						// checking if the list has been filled
						if (num_apps%(REALLOC_STEP) == 0)
							// if yes, then resize the list using realloc
							*app_list = resize_list(*app_list, num_apps+REALLOC_STEP+1);
						// use the extracted data to build an object which is an element
						// of the list
						update_app_node(*app_list + num_apps, ln_one, ln_three, strtol(ln_two, &dummy, 10));
						// increment the number of applications recorded
						num_apps++;

					}
				}
			}
			// if the line read matches the regex condition representing
			// the line representing the tracker entry:
			else if (!regexec(&tracker_entry_r, ln_one, 0, NULL, 0)) {

				// trim the newline character from the line
				ln_one[strlen(ln_one)-1] = '\0';
				// extract the tracker name into the same buffer
				memmove(ln_one, ln_one + 35, sizeof(ln_one) - 35);
				// insert the tracker entry into the trie structure,
				// which is explained in the corresponding header file
				insert_node(root_node, ln_one);

			}
		}
	}
	// if there was an error while opening the file:
	else {
		// exit, raising a process error
		perror("File error.");
	}

	// return the number of applications recorded, to be used later for sorting
	return num_apps;

}

// function that uses the built data structures to pretty print the results
int printer(trie_node* root_node, application_node* *app_list) {

	// creating a buffer to hold the tracker name
	char trie_op[TRACKER_SIZE];
	// a char just as a placeholder for spacing on the output
	char empty = ' ';
	// print statement for a header line
	printf("\nTracker Name       Number of occurrences\n\n");
	// print function to print all trie nodes
	display_all_nodes(root_node, trie_op, 0);

	// printing newline to separate result categories
	printf("\n");

	// print statement for the next header line
	printf("\nApp signature%*cApp name%*cTracker count\n\n", SIGNATURE_SIZE - 9, empty, APPLICATION_SIZE - 21, empty);
	// an iterating block to print the list of applications
	for (int i = 0; i < APPS_TO_DISPLAY; i++) {
		// formatted print statement to print details of each application;
		// using typecast to int to avoid warning
		printf("%s    %s%*d\n", (*app_list + i)->app_signature, (*app_list + i)->app_name, (int)(APPLICATION_SIZE-strlen((*app_list + i)->app_name)), (*app_list + i)->count_trackers);
	}

	// end normally
	return 0;

}


/***********************************************************************
* Main function
***********************************************************************/

// the function that invokes all this pizazz :)
int main(int argc, char **argv) {

	// file pointer for the logfile
	FILE *logfile;
	// creating the root node for the trie structure
	trie_node *root_node = generate_node();
	// creating the application list with an initial size equal to the reallocation
	// parameter defined above
	application_node *app_list = (application_node*)malloc(REALLOC_STEP * sizeof(application_node));
	// the number of applications, which is to be recieved from the parsing function
	long int num_apps;

	// if there are correct number of arguments specified then:
	if (argc == 2) {

		// open up the given logfile
		logfile = fopen(argv[1], "r");
		// parse the logfile using the parsing function defined above
		num_apps = parser(logfile, root_node, &app_list);
		// close the logfile
		fclose(logfile);
		// sort the list of applications using stdlib's qsort function
		qsort(app_list, num_apps, sizeof(application_node), compare);
		// print the result using the printing function defined above
		printer(root_node, &app_list);


	}
	// if incorrect number of arguments specified then:
	else {

		// print error message
		printf("Too many or too few arguments specified.\n");
		// and then exit
		exit(0);

	}

	// terminate normally
	return 0;

}