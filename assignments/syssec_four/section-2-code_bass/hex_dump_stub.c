/***********************************************************************
* FILENAME : hex_dump_stub.c
*
* DESCRIPTION :
*       A program that generates the hex dump of any given file.
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
#include <ctype.h>
#include <unistd.h>

// include custom header files; refer respective files for further 
// explanation
#include "./include/hex_dump_helper.h"


/***********************************************************************
* Main function
***********************************************************************/

// hit or miss, i guess they never miss
int main(int argc, char **argv) {

	// checking for correct number of arguments
	if (argc != 2) {
		// if not, print error message and exit
		printf(
			"Incorrect command usage.\n"
			"Usage: hex_dump_stub [FILENAME]\n\n"
		);
		exit(1);
	}

	// checking if the file path is valid
	if (access(argv[1], F_OK) != -1)
		// if yes, then display the hex dump
		hex_dump(argv[1]);
	else
		// if not, them print the relevant error message
		printf("File access error!\n");

	return 0;

}