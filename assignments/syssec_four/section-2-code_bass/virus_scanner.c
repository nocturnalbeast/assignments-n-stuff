/***********************************************************************
* FILENAME : virus_scanner.c
*
* DESCRIPTION :
*       A scanning program that checks all the files in a directory
*       for changes made into a file, anc checks it against specific
*       signatures, to see if the files which have been tampered with
*       are "viruses" or not.
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
#include <getopt.h>
#include <openssl/md5.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <signal.h>
#include <ctype.h>

// include custom header files; refer respective files for further 
// explanation
#include "./include/hex_dump_helper.h"


/***********************************************************************
* User parameters
***********************************************************************/

// the length of the file path, pretty self-explanatory
#define FILE_PATH_LEN 128
// the length of the block read for MD5 computation
#define MD5_BLOCK_LENGTH 512
// the length of the MD5 digest string, plus one extra space for the
// string termination character
#define MD5_SUM_LEN 33
// the default time interval (in seconds) between two consecutive
// rounds of scanning
#define DEF_SCAN_INTERVAL 10
// increment step for increasing the length of the list
#define REALLOC_STEP 2
// a dummy character for pretty printing
#define EMPTY_CHAR ' '
// the length of the signature to be checked in suspicious files
#define SIGN_LEN 6
// the individual bytes which make up the signature;
// do note that a change in the length will require a change in the
// signature_search function (nothing too much, just a trivial change)
#define SIGN_BYTE_ONE 0xDE
#define SIGN_BYTE_TWO 0xAD
#define SIGN_BYTE_THREE 0xBE
#define SIGN_BYTE_FOUR 0xEF
#define SIGN_BYTE_FIVE 0xDE
#define SIGN_BYTE_SIX 0xAD


/***********************************************************************
* Basic structure definitions
***********************************************************************/

typedef struct scan_file {
	char full_path[FILE_PATH_LEN];
	char md5_sum[MD5_SUM_LEN];
} scan_file;


/***********************************************************************
* The hashing function and its helper functions
***********************************************************************/

// function to generate the MD5sum of a file, given its filename
void generate_md5(char* file_path, unsigned char *md5_sum) {

	// the context object for MD5 computation, see MD5 implementation
	MD5_CTX context;
	// the buffer that stores each block
	char buffer[MD5_BLOCK_LENGTH];
	// the counter that keeps track of the number of bytes that's been
	// already read
	size_t bytes_read;

	// file in question for which the MD5 digest needs to be generated
	int file_to_md5 = open(file_path, O_RDONLY);

	// initalizing the MD5 context, see MD5 implementation
	MD5_Init(&context);
	// reading the first block before going into actual MD5 computation
	bytes_read = read(file_to_md5, buffer, MD5_BLOCK_LENGTH);

	// loop to read each block and do whatever ;)
	while (bytes_read > 0) {
		MD5_Update(&context, buffer, bytes_read);
		bytes_read = read(file_to_md5, buffer, MD5_BLOCK_LENGTH);
	}

	// final computation and store to the char buffer for MD5 digest
	MD5_Final(md5_sum, &context);

}

// helper function to print the MD5 digest
void print_md5(unsigned char* md5_sum) {

	// loop to print as hex characters
	for(int i=0; i <MD5_DIGEST_LENGTH; i++)
		printf("%02x", md5_sum[i]);
	// a final newline character for that weird shell behavior
	printf("\n");

}

// helper function to convert result of MD5 generation to readable
// hex format
void convert_md5sum(unsigned char* md5_sum, char* md5_string) {

	// loop to convert into hex characters
	for (int chr_idx = 0; chr_idx < MD5_DIGEST_LENGTH; chr_idx++)
		// using snprintf with shifting bounds to convert the unsigned
		// char string to the readable string format
		snprintf(md5_string + (2*chr_idx), MD5_DIGEST_LENGTH*2, "%02x", md5_sum[chr_idx]);

}

// function to compare two MD5 digests, where one is the plain digest
// and the other is the result obtained from the digest generation
// function
int md5_compare(char* md5_string, unsigned char* md5_sum) {

	// just checking for null strings here
	if (!md5_string || !md5_sum)
		return -1;

	// a string buffer for the converted unsigned char result
	char md5_sum_string[MD5_SUM_LEN];

	// loop to convert into hex characters
	for (int chr_idx = 0; chr_idx < MD5_DIGEST_LENGTH; chr_idx++)
		// using snprintf with shifting bounds to convert the unsigned
		// char string to the readable string format
		snprintf(md5_sum_string + (2*chr_idx), MD5_DIGEST_LENGTH*2, "%02x", md5_sum[chr_idx]);

	// just return whatever's the strcmp result, we'll use that,
	// since if both strings are the same it'll return zero
	return strcmp(md5_string, md5_sum_string);

}


/***********************************************************************
* Helper functions for scan environment construction
***********************************************************************/

// simple wrapper for realloc to resize the dynamically allocated list
scan_file* resize_list(scan_file* scan_list, int size) {

	scan_file* list_resized = (scan_file*)realloc(scan_list, size * sizeof(scan_file));
	return list_resized;

}

// function to construct the list of all the files that are to be
// scanned, which is later used as the reference by the scanning
// function
void build_scanlist(char* scan_directory, scan_file** scan_list, int* num_files, int recursive_flag) {

    // the directory structure that will be used to handle the current
    // directory and the accompanying directory entry structure
	DIR *directory;
	struct dirent *directory_entry;
	// the full path to the file that will be resolved with path
	// expansion
	char resolved_scan_dir[FILE_PATH_LEN];
	// a buffer for the MD5 generation output
	unsigned char md5_buffer[MD5_DIGEST_LENGTH];

    // checking if the directory exists
	if ((directory = opendir(scan_directory)) != NULL) {

        // if yes, then resolve the full path of the directory
		realpath(scan_directory, resolved_scan_dir);
		// while the next file exists in the directory
		while ((directory_entry = readdir(directory)) != NULL) {

            // resizing the list, should it run out of space
			if ((*num_files)%(REALLOC_STEP) == 0)
				*scan_list = resize_list(*scan_list, (*num_files)+REALLOC_STEP+1);

            // if the directory entry is a file
			if (directory_entry->d_type == DT_REG) {
				// concatenate the file path and the file name
				// and store it in the structure object
				snprintf((*scan_list+(*num_files))->full_path, FILE_PATH_LEN, "%s/%s", resolved_scan_dir, directory_entry->d_name);
				// generate the MD5 digest using the newly generated
				// file path
				generate_md5((*scan_list+(*num_files))->full_path, md5_buffer);
				// convert the digest obtained into the hex string
				// and store it in the structure object
				convert_md5sum(md5_buffer, (*scan_list+(*num_files))->md5_sum);
				// increment the number of files after all this
				(*num_files)++;
			}
			// if the directory entry is a folder;
			// then we do one of two things, either include all the
			// files in that directory as well, should the recursive
			// flag be set, or just ignore it, if the former is not set
			else if ((recursive_flag == 1) && (directory_entry->d_type == DT_DIR)) {
				// making sure to avoid the current directory and parent
				// directory entries
				if ((strcmp(directory_entry->d_name, "..") != 0) && (strcmp(directory_entry->d_name, ".") != 0)) {
				// appending the directory name to the path
				snprintf(scan_directory, FILE_PATH_LEN, "%s/%s", resolved_scan_dir, directory_entry->d_name);
				// then calling this function recursively with the new path
				build_scanlist(scan_directory, scan_list, num_files, recursive_flag);
				}
			}

		}

        // finally closing the directory
		closedir(directory);

	}
	// now if the directory doesn't exist, then
	else {

        // just issue an error statement, and then exit
		printf("The directory does not exist! Quitting now.\n");
		exit(1);

	}

}


/***********************************************************************
* Scanning function and its helper functions
***********************************************************************/

// simple function to check whether the user wants to continue with
// execution or not
void scan_prompt() {

	printf("\nPress ENTER to start scanning:\n");
	if (getchar() != '\n')
		exit(0);

}

// function that checks whether the specified signature is present in
// the file or not
int signature_search(scan_file* scan_file) {

    // the signature bytes converted into a character array and the
    // current character being read
	char signature[] = {SIGN_BYTE_ONE, SIGN_BYTE_TWO, SIGN_BYTE_THREE, SIGN_BYTE_FOUR, SIGN_BYTE_FIVE,SIGN_BYTE_SIX}, current_char;
	// variables to keep track of position of the pointer, and
	// one to act like a state machine, which increments with each
	// consecutive character match
	int position = 0, sub_matches = 0;
	// the length of the file
	long len_file;

    // the file pointer that points to the file that needs to be
    // checked for existence of the signature
	FILE *suspect_file = fopen(scan_file->full_path, "r");

    // go to the end of the file
	fseek(suspect_file, 0, SEEK_END);
	// then get length of the file from current position
	len_file = ftell(suspect_file);
	// then go back to the start of the file
	rewind(suspect_file);

    // while the position hasn't exceeded the length of the file
	while (position <= len_file) {
	    // read a character from the file
		current_char = getc(suspect_file);
		// increment the position
		position++;

        // if the character read matches the character in the
        // signature respective to the state of the signature
        // match, then
		if (current_char == signature[sub_matches]) {
			// increment the state (proceed to the next state)
			sub_matches++;
			// if the state moves to completion, then
			if (sub_matches >= SIGN_LEN) {
			    // close the file
				fclose(suspect_file);
				// and return 1, for the signature has been found
				return 1;
			}
		}
		// if a match hasn't been found until now, then
		else {
		    // close the file
			fclose(suspect_file);
			// and return 0, for the signature is not present
			// in the file
			return 0;
		}
	}

	return 0;

}

// function to print the infected file's details
void print_infected(scan_file* infected_file, int verbose_flag) {

	// the buffers to store the original and the modified MD5 digests
	unsigned char md5_buffer[MD5_DIGEST_LENGTH];
	char md5_sum[MD5_SUM_LEN], md5_sum_ori[MD5_SUM_LEN];
	// generate the modified MD5 values
	generate_md5(infected_file->full_path, md5_buffer);
	// convert it to the format we see
	convert_md5sum(md5_buffer, md5_sum);
	// store the original MD5 digest into respective buffer
	strcpy(md5_sum_ori, infected_file->md5_sum);
	// store the modified MD5 digest into respective buffer
	strcpy(infected_file->md5_sum, md5_sum);

	// print block to tell the user that an file has been found
	printf("\nFound infected file at %s!\n", infected_file->full_path);
	// print block to display more data in case the verbose flag is
	// set
	if (verbose_flag) {
		printf("Original MD5: %s\n", md5_sum_ori);
		printf("Modified MD5: %s\n", md5_sum);
		printf("\nHex dump of file:\n\n");
		hex_dump(infected_file->full_path);
	}

}

// function that does one round of scanning
void scan_round(scan_file* scan_list, int num_files, int verbose_flag) {

	// a buffer for MD5 comaparison
	unsigned char md5_buffer[MD5_DIGEST_LENGTH];
	// iterating through all the files
	for (int idx = 0; idx < num_files; idx++) {
		// generate the MD5 for the given file
		generate_md5((scan_list+idx)->full_path, md5_buffer);
		// if it doesn't match with the existing MD5, then
		if ((md5_compare((scan_list+idx)->md5_sum, md5_buffer)) != 0) {
			// run a signature search, and if that returns positive
			if (signature_search(scan_list+idx))
				// use the helper function to display the infected file
				print_infected((scan_list+idx), verbose_flag);
		}
	}

}


/***********************************************************************
* Other accompanying functions
***********************************************************************/

// a function that prints a message on how to use the executable
void usage() {

	printf(
		"Usage: virus_scanner [OPTION] [ARGUMENT]...\n\n"
		"    -h, --help                           Show this help dialog and exit.\n"
		"\n"
		"  Scanning options:\n\n"
		"    -d, --directory DIRECTORY_PATH       The directory which contains the files to be scanned.\n"
		"    -i, --interval SECONDS               Set the time between rounds to a specified number of seconds, rather than the default value.\n"
		"    -r, --recursive                      Enable scanning of all files in sub-directories.\n"
		"\n"
		"  Output options:\n\n"
		"    -v, --verbose                        Show details of the scanning operation.\n"
		"\n"
	);

}

// a function that pretty prints all the entries populated, once the
// list is built; called only when verbose flag is set
void print_entries(scan_file* scan_list, int num_files) {

	// printing header lines
	printf("\nInitial construction complete, %d files scanned.\n\n", num_files);
	printf("File name%*cMD5 digest\n\n", (int)(FILE_PATH_LEN)-41, EMPTY_CHAR);
	// then pretty printing each entry with each iteration
	for (int idx = 0; idx < num_files; idx++)
		printf("%s%*s\n", (scan_list+idx)->full_path, (int)(FILE_PATH_LEN-strlen((scan_list + idx)->full_path)), (scan_list+idx)->md5_sum);

}

// function to handle keyboard interrupt
void exit_listener(int signal) {
	
	// display the exit message,
	printf(
		"\nTermination signal recieved."
		"\nThe program will now terminate."
		"\nBye!\n\n"
	);
	// then exit, what else?
	exit(0);

}


/***********************************************************************
* Main function
***********************************************************************/

// surprised pikachu isn't dead :0
int main(int argc, char **argv) {

	// choice value for getopt
	int ch;

	// the other values initalized by the getopt loop;
	// the flag to enable/disable verbose output,
	int verbose_flag = 0;
	// the directory whose files are scanned,
	char scan_directory[FILE_PATH_LEN];
	// the time between each consecutive round of scanning,
	double interval = DEF_SCAN_INTERVAL;
	// flag to enable/disable the "full-depth" or "surface" search
	// which is just a fancy way for saying recursive listing, but hey,
	// this is a virus scanner, has to have appeal :)
	int recursive_flag = 0;

	// options for getopt
	const char *short_options = "hd:i:s:rv";
	// the longer alternatives, these can also be used
	static struct option long_options[] = {
		{"help",          no_argument,        0, 'h'},
		{"directory",     required_argument,  0, 'd'},
		{"interval",      required_argument,  0, 'i'},
		{"recursive",     no_argument,        0, 'r'},
		{"verbose",       no_argument,        0, 'v'},
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
			// case to get the path to the directory to scan
			case 'd':
				strcpy(scan_directory, optarg);
				break;
			// case to set the interval of scan rounds
			case 'i':
				interval = atol(optarg);
				break;
			// case to set the mode of scanning
			case 'r':
				recursive_flag = 1;
				break;
			// case to set the verbosity
			case 'v':
				verbose_flag = 1;
				break;
			// cases for mangled arguments
			case '?':
			default:
				printf("%s: invalid option -%c.\n", argv[0], optopt);
				printf("Try `%s --help' for more information.\n", argv[0]);
				return -2;
		};
	};

    // count variable for the number of files scanned
	int num_files = 0;
	// the list that keeps track of the files
	scan_file* scan_list = (scan_file*)malloc(REALLOC_STEP*sizeof(scan_file));
	// then call the function to parse the directory tree and
	// build the list
	build_scanlist(scan_directory, &scan_list, &num_files, recursive_flag);

    // if the verbose flag is set, then
	if (verbose_flag == 1)
		// print the details of the files
		print_entries(scan_list, num_files);
	// if not, then
	else
		// just print a completion message
		printf("\nInitial construction complete.\n");

	// display a prompt to start scanning or to quit
	scan_prompt();
	// register the listener for interrupt
	signal(SIGINT, exit_listener);

	// finally run the scanning function repeatedly
	while(1) {
		scan_round(scan_list, num_files, verbose_flag);
		sleep(interval);
	}


}