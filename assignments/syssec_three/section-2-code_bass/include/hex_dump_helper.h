/***********************************************************************
* FILENAME : hex_dump_helper.h
*
* DESCRIPTION :
*       The header file that contains the implementation of a simple
*       hex dump utility and its helper functions.
*
***********************************************************************/


/***********************************************************************
* User parameters
***********************************************************************/

// the display offset for the hex characters, increase/decrease for
// indentation
#define HEX_START_POINT 1
// the spacing between the hex section and the ASCII section
#define ASCII_START_POINT 51
// the number of characters to be displayed in one line
#define NUM_CHARS 16
// the size of the line buffer
#define LINE_SIZE 100


/***********************************************************************
* Helper functions
***********************************************************************/

// function to reset the line
void clear_line(char *line, int size) {

	for (int line_idx = 0; line_idx < size; line_idx++)
		line[line_idx] = ' ';

}

// function to convert the characters into a printable format for the
// ASCII section
char* convert_to_printable(char *position, int c) {

	if (!isprint(c))
		c = '.';
	sprintf(position, "%c", c);
	return (++position);

}

// function to get the hex section into the line
char* get_hex(char *position, int c) {

	sprintf(position, "%02x ", (unsigned char) c);
	*(position+3)=' ';
	return (position+3);

}


/***********************************************************************
* The actual hex dump function
***********************************************************************/

// I needn't say this again.
void hex_dump(char *filename) {

	int c = ' ';
	char *hex_offset, *ascii_offset;
	FILE *ptr;
	char line[LINE_SIZE];

	ptr = fopen(filename,"r");

	while (c != EOF) {

		clear_line(line, sizeof line);
		hex_offset = line + HEX_START_POINT;
		ascii_offset = line + ASCII_START_POINT;

		while (ascii_offset < line + ASCII_START_POINT + NUM_CHARS && (c = fgetc(ptr)) != EOF) {
			hex_offset = get_hex(hex_offset, c);
			ascii_offset = convert_to_printable(ascii_offset, c);
		}

		printf("%s\n", line);

	}

	fclose(ptr);

}