/***********************************************************************
* FILENAME : infector_mini.c
*
* DESCRIPTION :
*       A program that injects certain signature into a specified file.
*       Minimal version of infector.c .
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
#include <unistd.h>


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


/***********************************************************************
* Main function (the only function :0)
***********************************************************************/

int main(int argc, char **argv) {

	// checking for correct number of arguments
	if (argc != 3) {
		// if not, print error message and exit
		printf(
			"Incorrect command usage.\n"
			"Usage: infector_mini [FILENAME] [SIGNATURE]\n\n"
		);
		exit(1);
	}

	// checking if the file path is valid
	if (access(argv[1], F_OK) != -1) {

        FILE *inject_file = fopen(argv[1], "ab");
        int sign_len = strlen(argv[2]);
        int idx = 0;
        char byte_buffer[5];
        unsigned int bin_data;
	    while(idx < sign_len){
            snprintf(byte_buffer, 5, "0x%c%c", *(argv[2]+idx), *(argv[2]+idx+1));
            sscanf(byte_buffer, "%x", &bin_data);
            fwrite(&bin_data, 1, 1, inject_file);
            idx += 2;

        }
	
	    fclose(inject_file);

    }
	else
		// if not, them print the relevant error message
		printf("File access error!\n");

	return 0;

}