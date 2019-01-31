/***********************************************************************
* FILENAME : unshadow.c
*
* DESCRIPTION :
*       A password cracker used to crack passwords of Linux accounts
*       given the passwd and shadow file, by running the hashes
*       against a given dictionary file.
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
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <crypt.h>
#include <unistd.h>
#include <math.h>
#include <ctype.h>
#include <time.h>

// include custom header files; refer respective files for further 
// explanation
#include "./include/user_helper.h"
#include "./include/cracker.h"


/***********************************************************************
* User parameters
***********************************************************************/

// increment step for increasing the length of the list
#define REALLOC_STEP 4
// maximum size of a line in the shadow file
#define SHADOW_L_SIZE 70
// maximum size of a line in the passwd file
#define PASSWD_L_SIZE 120
// the character delimiter used in the passwd and shadow files,
// usually ':'
#define CHAR_DELIM ":"
// the character delimiter used in the password hash field, usually '$'
#define HASH_DELIM "$"


/***********************************************************************
* Accompanying functions
***********************************************************************/

// a function that prints a message on how to use the executable
void usage() {

	printf(
		"Usage: unshadow [OPTION] [ARG]...\n\n"
		"    -h, --help                           Show this help dialog and exit.\n"
		"\n"
		"  Input options:\n\n"
		"    -p, --passwd PASSSWD_FILE            The passwd file containing the user entries, to use with the program.\n"
		"    -s, --shadow SHADOW_FILE             The shadow file corresponding to the passwd file, to use with the program.\n"
		"    -d, --dictionary DICTIONARY_FILE     The dictionary file to use with the program.\n"
		"\n"
		"  Output options:\n\n"
		"    -o, --output OUTPUT_FILE             The file to write the username and password combinations to.\n"
		"\n"
		"  Operational options:\n\n"
		"    -v, --verbose                        Show details of the cracking operation.\n"
		"    -c, --caching                        Enable cracking mode to improve the speed of cracking in certain cases.\n"
		"    -u, --username                       Enable the username cracker to test all variants of the username (the user's actual name).\n"
	);

}

// a helper function that extracts the data from the line read from the
// passwd file and updates the user entry with the entries so gained
void extract_passwd(char *buf_passwd, user *user_entry) {

	char *token, tokenized[7][PASSWD_L_SIZE];
	int i = 0;

	while ((token = strtok_r(buf_passwd, CHAR_DELIM, &buf_passwd))) {
		strcpy(tokenized[i], token);
		i++;
	}

	update_user_passwd(user_entry, tokenized[0], tokenized[4], tokenized[5], tokenized[6], strtol(tokenized[2], NULL, 10), strtol(tokenized[3], NULL, 10));

}

// a helper function that extracts the data from the line read from the
// shadow file and updates the user entry with the entries so gained
void extract_shadow(char *buf_shadow, user *user_entry) {

	char *token_one, *token_two, tokenized[3][SHADOW_L_SIZE];
	int i = 0;

	while ((token_one = strtok_r(buf_shadow, CHAR_DELIM, &buf_shadow))) {
		if (i == 1)
			break;
		i++;
	}

	i = 0;
	while ((token_two = strtok_r(token_one, HASH_DELIM, &token_one))) {
		strcpy(tokenized[i], token_two);
		i++;
	}

	update_user_shadow(user_entry, tokenized[0], tokenized[2], tokenized[1]);

}

// the function that goes through the passwd file and the shadow file and
// builds the list of users as a dynamic array of struct objects
user* build_list(FILE *passwd_file, FILE *shadow_file, int *num_users) {

	user* user_list = (user*)malloc(REALLOC_STEP*sizeof(user));

	if (passwd_file != NULL && shadow_file != NULL) {

		char buf_passwd[PASSWD_L_SIZE], buf_shadow[SHADOW_L_SIZE];

		while ((fgets(buf_passwd, PASSWD_L_SIZE, passwd_file) != NULL) && (fgets(buf_shadow, SHADOW_L_SIZE, shadow_file) != NULL)) {

			// fix the line endings
			buf_passwd[strlen(buf_passwd)-1] = '\0';
			buf_shadow[strlen(buf_shadow)-1] = '\0';

			if ((*num_users)%(REALLOC_STEP) == 0)
				user_list = resize_list(user_list, (*num_users)+REALLOC_STEP+1);

			extract_passwd(buf_passwd, user_list+(*num_users));
			extract_shadow(buf_shadow, user_list+(*num_users));

			(*num_users)++;

		}

	}

	return user_list;

}


/***********************************************************************
* Main function
***********************************************************************/

// the function that does it all :)
int main(int argc, char **argv) {

	// recording the starting time of the program
	clock_t start_time = clock();

	// file pointers for input and output files
	FILE *passwd_file, *shadow_file, *dict_file, *output_file;

	// number of users in the lists
	int num_users = 0;

	// variables for tracking stats of cracking operations
	int crack_status = 0, crack_count = 0;

	// the list that will contain the user entries from the input files
	user *user_list;

	// choice values and flag (for verbose display) for getopt
	int ch, verbose_flag = 0;

	// flag variables for mode switches and cracker options
	int cache_mode_flag = 0, gecos_flag = 0;

	// options for getopt
	const char *short_options = "vcuhp:s:d:o:";
	// the longer alternatives, these can also be used
	static struct option long_options[] = {
		{"verbose",     no_argument,        0, 'v'},
		{"caching",     no_argument,        0, 'c'},
		{"username",    no_argument,        0, 'u'},
		{"help",        no_argument,        0, 'h'},
		{"passwd",      required_argument,  0, 'p'},
		{"shadow",      required_argument,  0, 's'},
		{"dictionary",  required_argument,  0, 'd'},
		{"output",      required_argument,  0, 'o'},
		{NULL, no_argument, NULL, 0}
	};

	// the getopt loop
	while ((ch = getopt_long(argc, argv, short_options, long_options, NULL)) != -1) {
		switch (ch)	{
			// just for the case wherein no more options are left
			case -1:
			// long options toggles
			case 0:
				break;
			// case to display help
			case 'h':
				usage();
				exit(0);
				break;
			// case to set the verbosity
			case 'v':
				verbose_flag = 1;
				break;
			// case to enable/disable caching mode
			case 'c':
				cache_mode_flag = 1;
				break;
			// case to enable/disable cracking with the constructed variants
			// of the usernames
			case 'u':
				gecos_flag = 1;
				break;
			// case to get the passwd file as optarg
			case 'p':
				passwd_file = fopen(optarg, "r");
				break;
			// case to get the shadow file as optarg
			case 's':
				shadow_file = fopen(optarg, "r");
				break;
			// case to get the dictionary file as optarg
			case 'd':
				dict_file = fopen(optarg, "r");
				break;
			// case to get the output file as optarg
			case 'o':
				output_file = fopen(optarg, "w+");
				break;
			// cases for mangled arguments
			case '?':
			default:
				printf("%s: invalid option -%c.\n", argv[0], optopt);
				printf("Try `%s --help' for more information.\n", argv[0]);
				return -2;
		};
	};

	// generate the user list with the list building function
	user_list = build_list(passwd_file, shadow_file, &num_users);

	// buffers for the paths for the cache files for the dictionary 
	// attack and the GECOS variants attack
	char dict_hl_path[MAX_PATH_LEN], dict_pl_path[MAX_PATH_LEN];
	char uname_hl_path[MAX_PATH_LEN], uname_pl_path[MAX_PATH_LEN];

	// if caching is enabled,
	if (cache_mode_flag == 1) {

		// then iterate through all the users
		for (int i = 0; i < num_users; i++) {

			// build the paths for the cache files for the dictionary
			// attack
			snprintf(dict_hl_path, MAX_PATH_LEN, "%s%s%s-%s", DICTLIST_ROOT, HASHLIST_SUFFIX, (user_list+i)->password_type, (user_list+i)->password_salt);
			snprintf(dict_pl_path, MAX_PATH_LEN, "%s%s%s-%s", DICTLIST_ROOT, PLAINLIST_SUFFIX, (user_list+i)->password_type, (user_list+i)->password_salt);
			// check if the cache file exists, if not
			if (access(dict_hl_path, 0) != 0)
				// build the cache file for the user with the given dictionary
				cached_dictionary_builder(dict_file, user_list+i, dict_hl_path, dict_pl_path);

			// run the cached version of the dictionary attack
			crack_status = cached_cracker(user_list+i, output_file, dict_hl_path, dict_pl_path, verbose_flag);

			// if the user's password hasn't been cracked and if the GECOS variant
			// attack is enabled then
			if (crack_status != 1 && gecos_flag == 1) {
				
				// build the path prefixes for the cache files for the
				// GECOS variant attack
				snprintf(uname_hl_path, MAX_PATH_LEN, "%s%s%s-%s", PERSLIST_ROOT, HASHLIST_SUFFIX, (user_list+i)->password_type, (user_list+i)->password_salt);
				snprintf(uname_pl_path, MAX_PATH_LEN, "%s%s%s-%s", PERSLIST_ROOT, PLAINLIST_SUFFIX, (user_list+i)->password_type, (user_list+i)->password_salt);
				
				// run the cache generation for the user
				cached_gecos_builder(user_list+i, uname_hl_path, uname_pl_path);
				// then run the cached version of the GECOS variant attack
				crack_status = cached_gecos_cracker(user_list+i, uname_hl_path, uname_pl_path, output_file, verbose_flag);

			}

			// increment the count of users cracked, if successful
			crack_count += crack_status;
		
		}

	}

	// if the caching mode isn't enabled, then
	else {

		// then iterate through all the users
		for (int i = 0; i < num_users; i++) {

			// run the dictionary attack for the given user
			crack_status = simple_cracker(user_list+i, output_file, dict_file, verbose_flag);

			// if that hasn't worked and if the GECOS variant cracking
			// attack is enabled then
			if (crack_status != 1 && gecos_flag == 1)
				// run the GECOS variant cracking attack on the given user
				crack_status = gecos_cracker(user_list+i, output_file, verbose_flag);

			// increment the count of users cracked, if successful
			crack_count += crack_status;

		}

	}

	// recording the ending time of the program
	clock_t end_time = clock();

	// print the number of accounts cracked and the time taken
	if (verbose_flag) {
		printf("\nTotal accounts cracked: %d", crack_count);
		printf("\nTotal time taken: %f seconds", (double)(end_time - start_time) / CLOCKS_PER_SEC);
		printf("\n");
	}
	
	// finally exit :0
	return 0;

}