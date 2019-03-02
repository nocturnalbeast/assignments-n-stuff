/***********************************************************************
* FILENAME : the_buster.c
*
* DESCRIPTION :
*       A program that does a variety of stuff, including reading a 
*       hello-world program, looks for bin files and replaces its
*       content with the hello-world program, and replaces the hello
*       world message with any string.
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
#include <getopt.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>

// include custom header files; refer respective files for further 
// explanation
#include "./include/hex_dump_helper.h"

/***********************************************************************
* User parameters
***********************************************************************/

// the length of the file path, pretty self-explanatory
#define FILE_PATH_LEN 128
// the size of the file copy buffer
#define FILE_COPY_BUFLEN 8192
// a dummy character for pretty printing
#define EMPTY_CHAR ' '
// the extension to be "busted"
#define CHOSEN_FILE_EXT ".bin"
// the file path to the temporary file that contains the modified hello
// world executable
#define TEMP_MOD_FPATH "./mod_hello"
// the data that would be replaced in place of the hello world message
#define MOD_DATA "BUSTED"
// the data that needs to be replaced with the MOD_DATA message
#define ORI_DATA "Hi World"

/***********************************************************************
* Other accompanying functions
***********************************************************************/

// a function that prints a message on how to use the executable
void usage() {

	printf(
		"Usage: the_buster [OPTION] [ARGUMENT]...\n\n"
		"    -h, --help                           Show this help dialog and exit.\n"
		"\n"
		"  Usage options:\n\n"
		"    -f, --file HELLO_WORLD_FILE          The path to the hello-world executable.\n"
		"    -d, --directory DIRECTORY            The directory to look for *.bin files.\n"
        "\n"
	);

}


/***********************************************************************
* Helper functions
***********************************************************************/

// function to compare the file extension to see whether the file is
// the one we need to "bust"
int check_file_extension(char* file_name, char* file_ext) {

	// get the length
	int len_str = strlen(file_name);
	// get up to the point of the period symbol separating the filename
	// and the extension
	while (*(file_name + len_str) != '.')
		len_str--;
	// compare the two strings
	return strcmp((file_name + len_str), file_ext);

}

// function to generate the "busted" executable
void gen_modified_exec(char* hello_path) {

	// file pointer to the hello-world executable
	FILE *hello_file = fopen(hello_path, "rb");
	// file pointer to the temporary modified executable
	FILE *mod_file = fopen(TEMP_MOD_FPATH, "wb+");

	// if any errors happen while opening the files
	if ((mod_file == NULL) || (hello_file == NULL)) {
		// show error message and exit
		perror("Errors occured in copy. Exiting now.\n");
		exit(EXIT_FAILURE);
	}

	// buffer to read line from the source
	char line_buffer[FILE_COPY_BUFLEN];
	// pointer to point to the start of the hello world message
	char *find_ptr;
	// length of line containing the hello world message
	int len_ori_msg;
	// parts of the line before and after the hello world message
	char part_one[FILE_COPY_BUFLEN], part_two[FILE_COPY_BUFLEN];

	// while the end of the file hasn't been reached
	while (fgets(line_buffer, FILE_COPY_BUFLEN, hello_file) != NULL) {
		// find the substring corresponding to the hello world message
		find_ptr = strstr(line_buffer, ORI_DATA);
		// if found
		if (find_ptr != NULL) {
			// find the length of the line containing the message
			len_ori_msg = strlen(ORI_DATA);
			// copy the text before it to a buffer
			strncpy(part_one, line_buffer, find_ptr - line_buffer);
			// copy the text after it to another buffer
			strcpy(part_two, (find_ptr + len_ori_msg));
			// combine it together with the modified (busted) message
			snprintf(line_buffer, FILE_COPY_BUFLEN, "%s%s%s", part_one, MOD_DATA, part_two);
		}
		// write the line to the modified file
		fputs(line_buffer, mod_file);
	}

	// close both the files
	fclose(hello_file);
	fclose(mod_file);

}

// function that emulates "chmod +x [FILENAME]"
void give_execute_permissions(char* full_path) {

	// get the properties of the file
	struct stat file_stat;
	stat(full_path, &file_stat);
	// then add execute permissions to the original mode
	chmod(full_path, file_stat.st_mode | S_IXUSR | S_IXGRP | S_IXOTH);

}

// the function that actually orchestrates all this :0
void buster_function(char* search_directory, char* hello_path) {

	// stuff to keep track of the directory and its files
	DIR *directory;
	struct dirent *directory_entry;
	// the path buffers
	char full_path[FILE_PATH_LEN], resolved_search_dir[FILE_PATH_LEN];

	// if initial conditions are all right
	if (((directory = opendir(search_directory)) != NULL) && (access(hello_path, F_OK) != -1)) {

		// display the hex dump of the hello-world executable
		hex_dump(hello_path);
		// generate the temporary modifed executable
		gen_modified_exec(hello_path);

		// resolve the relative path and store it in a buffer
		realpath(search_directory, resolved_search_dir);
		// while there are still files present in the directory
		while ((directory_entry = readdir(directory)) != NULL) {
			// if the file is a normal one, not any directory or any special file
			if (directory_entry->d_type == DT_REG) {
				// then combine the resolved path and the file name into the
				// respective buffer
				snprintf(full_path, FILE_PATH_LEN, "%s/%s", resolved_search_dir, directory_entry->d_name);
				// if the generated path to the file is valid then
				if (access(full_path, F_OK) != -1) {
					// check the file extension to see if it's the one we need to
					// work on
					if(check_file_extension(directory_entry->d_name, CHOSEN_FILE_EXT) == 0) {
						
						// then just copy it over
						FILE *src_file, *dest_file;

						src_file = fopen(TEMP_MOD_FPATH, "rb");
						dest_file = fopen(full_path, "wb");

						if ((src_file == NULL) || (dest_file == NULL)) {
							perror("Errors occured in copy. Exiting now.\n");
							exit(EXIT_FAILURE);
						}

						size_t n, m;
						unsigned char buff[FILE_COPY_BUFLEN];
						do {
							n = fread(buff, 1, sizeof buff, src_file);
							if (n)
								m = fwrite(buff, 1, n, dest_file);
							else
								m = 0;
						} while ((n > 0) && (n == m));
						if (m)
							perror("Errors occured in copy.\n");

						fclose(src_file);
						fclose(dest_file);

						// finally add the execute permissions to the modified file
						give_execute_permissions(full_path);

					}
				}
				else
					printf("File access error!\n");
			}
		}

		// after all the required modifications are complete, then
		// close the directory
		closedir(directory);
		// and remove the temporary file made
		remove(TEMP_MOD_FPATH);

	}
	// if initial conditions weren't fulfilled, then
	else {

		// print the error message and then exit
		printf("The directory does not exist! Quitting now.\n");
		exit(EXIT_FAILURE);

	}

}

/***********************************************************************
* Main function
***********************************************************************/

// whew, this is getting tiring.....you don't say?
int main(int argc, char **argv) {

	// choice value for getopt
	int ch;

	// the other values initalized by the getopt loop;
	// buffer for the path to the hello-world executable
	char hello_path[FILE_PATH_LEN];
	// buffer for the search directory path
	char directory_path[FILE_PATH_LEN];

	// options for getopt
	const char *short_options = "hf:d:";
	// the longer alternatives, these can also be used
	static struct option long_options[] = {
		{"help",       no_argument,        0, 'h'},
		{"file",       required_argument,  0, 'f'},
		{"directory",  required_argument,  0, 'd'},
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
			// case to get the path to the hello-world executable
			case 'f':
				strcpy(hello_path, optarg);
				break;
			// case to get the path to "bust" the selected files
			case 'd':
				strcpy(directory_path, optarg);
				break;
			// cases for mangled arguments
			case '?':
			default:
				printf("%s: invalid option -%c.\n", argv[0], optopt);
				printf("Try `%s --help' for more information.\n", argv[0]);
				return -2;
		};
	};

	// just do it!
	buster_function(directory_path, hello_path);

}