/***********************************************************************
* FILENAME : infector.c
*
* DESCRIPTION :
*       A program that injects certain signature into a specified file
*       at any required point. This is to demonstrate the working of 
*       the scanner program.
*
* NOTES :
*       The explanation to most of the functionality is described
*       along with the code itself. Refer the comments accompanying
*       the code for the explanation.
*
* AUTHOR : nocturnalbeast
*
***********************************************************************/

// WARN : this is an incomplete version. Use infector_mini instead.
// TODO : fix injector
// TODO : build overwrite logic

/***********************************************************************
* Headers
***********************************************************************/

// include standard header files
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>


/***********************************************************************
* User parameters
***********************************************************************/

// the length of the file path, pretty self-explanatory
#define FILE_PATH_LEN 128
// the maximum length of the hex string which represents the binary
// data to be injected into the file
#define SIGN_MAX_LEN 100
// a dummy character for pretty printing
#define EMPTY_CHAR ' '
// 


/***********************************************************************
* Other accompanying functions
***********************************************************************/

// a function that prints a message on how to use the executable
void usage() {

	printf(
		"Usage: infector [OPTION] [ARGUMENT]...\n\n"
		"    -h, --help                           Show this help dialog and exit.\n"
		"\n"
		"  Usage options:\n\n"
		"    -f, --file FILE_TO_INFECT            The file to which the given signature is to be added to.\n"
		"    -s, --signature HEX_STRING           The binary data to be injected into the file provided.\n"
		"    -p, --position NUMBER                The position at which the given signature is to be inserted at. Not using this flag will result in the signature being appended to the file at the end.\n"
		"    -o, --overwrite                      Replace the existing data while writing the signature, instead of making space.\n"
        "\n"
	);

}


/***********************************************************************
* Injector functions and its accompanying functions
***********************************************************************/

// function to inject the given signature into a binary file
void inject_signature(char* file_path, char* signature, long sign_position) {

	FILE *inject_file = fopen(file_path, "ab");

	int sign_len = strlen(signature);
	char byte_buffer[5];
	
	unsigned int bin_data;

	long len_file;

    // go to the end of the file
	fseek(inject_file, 0L, SEEK_END);
	// then get length of the file from current position
	len_file = ftell(inject_file);

	printf("%ld\n", len_file);
	if (sign_position == 0)
		sign_position = len_file;
	else if (sign_position > len_file)
		sign_position = 0;

	fseek(inject_file, sign_position, SEEK_SET);

	int i = 0;
	while(i < sign_len){
		snprintf(byte_buffer, 5, "0x%c%c", *(signature+i), *(signature+i+1));
		sscanf(byte_buffer, "%x", &bin_data);
		fwrite(&bin_data, 1, 1, inject_file);
		i+=2;
	}
	
	fclose(inject_file);	

}

void overwrite_signature(char* file_path, char* signature, long sign_position) {
	printf("wololo");
}


/***********************************************************************
* Main function
***********************************************************************/

// guess i'll code ¯\_(ツ)_/¯
int main(int argc, char **argv) {

	// choice value for getopt
	int ch;

	// the other values initalized by the getopt loop;
    // the string buffer to store the path of the file to be infected
    char inf_file_path[FILE_PATH_LEN];
	// the binary data which is to be inserted into the provided file
	// in the format of a hex string
	char signature[SIGN_MAX_LEN];
    // the position of the file at which the signature is inserted
    long sign_position = 0;
    // the flag to enable/disable overwrite mode
    int overwrite_flag = 0;

	// options for getopt
	const char *short_options = "hf:s:p:o";
	// the longer alternatives, these can also be used
	static struct option long_options[] = {
		{"help",       no_argument,        0, 'h'},
		{"file",       required_argument,  0, 'f'},
		{"signature",  required_argument,  0, 's'},
		{"position",   required_argument,  0, 'p'},
		{"overwrite",  no_argument,        0, 'o'},
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
			// case to get the path to the file to infect
			case 'f':
				strcpy(inf_file_path, optarg);
				break;
			// case to recieve the binary data to be injected
			case 's':
				strcpy(signature, optarg);
				break;
			// case to set the position at which the signature is to be
            // inserted
			case 'p':
				sign_position = atol(optarg);
				break;
			// case to set the overwrite flag, thus enabling the overwrite
            // mode
			case 'o':
				overwrite_flag = 1;
				break;
			// cases for mangled arguments
			case '?':
			default:
				printf("%s: invalid option -%c.\n", argv[0], optopt);
				printf("Try `%s --help' for more information.\n", argv[0]);
				return -2;
		};
	};

    if (overwrite_flag)
		overwrite_signature(inf_file_path, signature, sign_position);
	else
		inject_signature(inf_file_path, signature, sign_position);


}