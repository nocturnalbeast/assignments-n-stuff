/***********************************************************************
* FILENAME : cracker.h
*
* DESCRIPTION :
*       This header file contains functions to compute hashes and
*       run attacks in a variety of modes, and helper functions 
*       for related operations as well.
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
* User parameters
***********************************************************************/

// the location where the cracker stores variants of the usernames
#define PERSLIST_ROOT "./bin/gecos_lists"
// the location where the cracker stores the cached lists which
// correspond to the dictionary entries
#define DICTLIST_ROOT "./bin/dictionary_lists"
// the location where the cracker stores variants of the password
// entries in the dictionary file
#define DICTVARLIST_ROOT "./bin/dict_variant_lists"
// the location where the cracker stores variants of the usernames
#define PERSLIST_ROOT "./bin/gecos_lists"
// the location where the generated hashlists are stored
#define HASHLIST_SUFFIX "/hashlists/"
// the location where the generated plainlists are stored
#define PLAINLIST_SUFFIX "/plainlists/"
// the size of an entry in the dictionary file
#define DICT_ENTRY_LEN 100
// a limit on the maximum number of variations that can be generated 
// from a name
#define MAX_VARIANTS 16384
// the limit on how many names can be present in the GECOS field
#define MAX_NAMES 10
// the position of the plaintext password in the dictionary file
#define DICT_PLAIN_POS 4
// the delimiter used to extract the plaintext password from the
// dictionary
#define DICT_DELIM "\t"
// the delimiter that is used to separate the cracked username and
// the plaintext password in the output file
#define OUTPUT_DELIM ":"
// the delimiter(s) that are used to extract the names from the GECOS
// field
#define GECOS_DELIM " ,"
// the maximum limit on the path lengths for the cached lists
#define MAX_PATH_LEN 300


/***********************************************************************
* Accompanying functions
***********************************************************************/

// a function to display the details of a user once the password of
// the user is found
void display_cracked_user(user* user_entry, char* password) {
	printf("Cracked user: %s\n", user_entry->name);
	printf("Password: %s\n", password);
	printf("\n");
}


/***********************************************************************
* Cracking functions
***********************************************************************/

// the basic dictionary cracker, which takes each user entry and runs
// it against the given dictionary file to try and crack the password
int simple_cracker(user* user_entry, FILE* output_file, FILE* dict_file, int verbose_flag) {
	
	int success_status = 0;

	char user_hash[PASS_TYPE_LEN+PASS_SALT_LEN+PASS_HASH_LEN+1], pass_ext[PASS_TYPE_LEN+PASS_SALT_LEN+1];
	snprintf(user_hash, PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s$%s", user_entry->password_type, user_entry->password_salt, user_entry->password_hash);
	snprintf(pass_ext, PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s", user_entry->password_type, user_entry->password_salt);

	char *buf_hash, buf_plain[DICT_ENTRY_LEN], *buf_inter, *token;

	struct crypt_data crypt_d;

	int i = 0;

	if (dict_file != NULL) {
		
		fseek(dict_file, 0, SEEK_SET);

		while(fgets(buf_plain, DICT_ENTRY_LEN, dict_file)) {

			crypt_d.initialized = 0;

			if (buf_plain[strlen(buf_plain)-1] == '\n')
				buf_plain[strlen(buf_plain)-1] = '\0';
			
			buf_inter = buf_plain;
			i = 0;
			while ((token = strtok_r(buf_inter, DICT_DELIM, &buf_inter))) {
				if (i == DICT_PLAIN_POS - 1)
					break;
				i++;
			}

			buf_hash = crypt_r(token, pass_ext, &crypt_d);

			if (!strcmp(buf_hash, user_hash)) {
				success_status = 1;
				fprintf(output_file, "%s:%s\n", user_entry->name, token);
				if (verbose_flag)
					display_cracked_user(user_entry, token);
				return success_status;
			}

		}

	}

	return success_status;

}

// the function that tries all possible variants of the names in the
// GECOS field to try and crack the password
int gecos_cracker(user* user_entry, FILE* output_file, int verbose_flag) {
	
	int success_status = 0;

	char user_hash[PASS_TYPE_LEN+PASS_SALT_LEN+PASS_HASH_LEN+1], pass_ext[PASS_TYPE_LEN+PASS_SALT_LEN+1];
	snprintf(user_hash, PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s$%s", user_entry->password_type, user_entry->password_salt, user_entry->password_hash);
	snprintf(pass_ext, PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s", user_entry->password_type, user_entry->password_salt);

	char gecos_field[GECOS_LEN], *gecos_inter;
	strcpy(gecos_field, user_entry->gecos);
	gecos_inter = gecos_field;

	char *token, tokenized[MAX_NAMES][GECOS_LEN];
	
	char gecos_variants[MAX_VARIANTS][GECOS_LEN];
	
	struct crypt_data crypt_d;
	char *hash_pass;

	int split_idx = 0;
	while ((token = strtok_r(gecos_inter, GECOS_DELIM, &gecos_inter))) {
		strcpy(tokenized[split_idx], token);
		for (int lower_idx = 0; tokenized[split_idx][lower_idx] != '\0'; lower_idx++)
			tokenized[split_idx][lower_idx] = tolower(tokenized[split_idx][lower_idx]);
		split_idx++;
	}

	for (int name_idx = 0; name_idx < split_idx; name_idx++) {

		strcpy(gecos_variants[0], tokenized[name_idx]);
		hash_pass = crypt_r(gecos_variants[0], pass_ext, &crypt_d);
		if (!strcmp(hash_pass, user_hash)) {
			success_status = 1;
			fprintf(output_file, "%s:%s\n", user_entry->name, gecos_variants[0]);
			if (verbose_flag)
				display_cracked_user(user_entry, gecos_variants[0]);
			return success_status;
		}

		for (int idx_one = 0; idx_one < strlen(gecos_variants[0]); idx_one++) {
			for (int idx_two = 0; idx_two < (int)pow(2, idx_one); idx_two++) {
				int generate_idx = (int)pow(2, idx_one) + idx_two;
				strcpy(gecos_variants[generate_idx], gecos_variants[idx_two]);
				gecos_variants[generate_idx][idx_one] = toupper(gecos_variants[generate_idx][idx_one]);
				hash_pass = crypt_r(gecos_variants[generate_idx], pass_ext, &crypt_d);
				if (!strcmp(hash_pass, user_hash)) {
					success_status = 1;
					fprintf(output_file, "%s:%s\n", user_entry->name, gecos_variants[generate_idx]);
					if (verbose_flag)
						display_cracked_user(user_entry, gecos_variants[generate_idx]);
					return success_status;
				}
			}
		}

	}

	return success_status;

}


/***********************************************************************
* Cache builders for cached versions of the cracking functions
***********************************************************************/

// the caching mechanism for the cached version of the dictionary
// attack
void cached_dictionary_builder(FILE* dict_file, user* user_entry, char* hashlist_path, char* plainlist_path) {
	
	char pass_ext[PASS_SALT_LEN+PASS_TYPE_LEN+2];
	char dict_entry_buf[DICT_ENTRY_LEN], *dict_entry_buf_inter;
	struct crypt_data crypt_d;

	char *plain_pass;
	char *hash_pass;

	FILE *hashlist = fopen(hashlist_path, "w+");
	FILE *plainlist = fopen(plainlist_path, "w+");

	snprintf(pass_ext, PASS_SALT_LEN+PASS_TYPE_LEN+2, "$%s$%s", user_entry->password_type, user_entry->password_salt);

	if (dict_file != NULL) {

		fseek(dict_file, 0, SEEK_SET);
		
		while (fgets(dict_entry_buf, DICT_ENTRY_LEN, dict_file) != NULL) {
			
			if (dict_entry_buf[strlen(dict_entry_buf)-1] == '\n')
				dict_entry_buf[strlen(dict_entry_buf)-1] = '\0';
			
			crypt_d.initialized = 0;
			int i = 0;
			dict_entry_buf_inter = dict_entry_buf;
			
			while ((plain_pass = strtok_r(dict_entry_buf_inter, DICT_DELIM, &dict_entry_buf_inter))) {
				if (i == DICT_PLAIN_POS - 1)
					break;
				i++;
			}

			hash_pass = crypt_r(plain_pass, pass_ext, &crypt_d);

			fprintf(hashlist, "%s\n", hash_pass);
			fprintf(plainlist, "%s\n", plain_pass);

		}

	}

	fclose(hashlist);
	fclose(plainlist);

}

// the caching mechanism for the cached version of the GECOS variants
// attack
void cached_gecos_builder(user* user_entry, char* hashlist_path_prefix, char* plainlist_path_prefix) {

	char gecos_field[GECOS_LEN], *gecos_inter;
	strcpy(gecos_field, user_entry->gecos);
	gecos_inter = gecos_field;

	char pass_ext[PASS_SALT_LEN+PASS_TYPE_LEN+2];
	snprintf(pass_ext, PASS_SALT_LEN+PASS_TYPE_LEN+2, "$%s$%s", user_entry->password_type, user_entry->password_salt);

	char tokenized[MAX_NAMES][GECOS_LEN], *token;

	FILE *hashlist, *plainlist;
	char username_hashlist_path[MAX_PATH_LEN], username_plainlist_path[MAX_PATH_LEN];

	char *hash_pass;
	struct crypt_data crypt_d;

	int split_idx = 0;
	while ((token = strtok_r(gecos_inter, GECOS_DELIM, &gecos_inter))) {
		strcpy(tokenized[split_idx], token);
		for (int lower_idx = 0; tokenized[split_idx][lower_idx] != '\0'; lower_idx++)
			tokenized[split_idx][lower_idx] = tolower(tokenized[split_idx][lower_idx]);
		split_idx++;
	}

	char gecos_variants[MAX_VARIANTS][GECOS_LEN];

	for (int name_idx = 0; name_idx < split_idx; name_idx++) {

		snprintf(username_hashlist_path, MAX_PATH_LEN, "%s-%s", hashlist_path_prefix, tokenized[name_idx]);
		snprintf(username_plainlist_path, MAX_PATH_LEN, "%s-%s", plainlist_path_prefix, tokenized[name_idx]);

		if ((access(username_hashlist_path, 0) != 0) && (access(username_plainlist_path, 0) != 0)) {
			
			hashlist = fopen(username_hashlist_path, "w+");
			plainlist = fopen(username_plainlist_path, "w+");
			
			strcpy(gecos_variants[0],tokenized[name_idx]);
			crypt_d.initialized = 0;
			hash_pass = crypt_r(gecos_variants[0], pass_ext, &crypt_d);
			fprintf(hashlist, "%s\n", hash_pass);
			fprintf(plainlist, "%s\n", gecos_variants[0]);

			for (int idx_one = 0; idx_one < strlen(gecos_variants[0]); idx_one++) {
				for (int idx_two = 0; idx_two < (int)pow(2, idx_one); idx_two++) {
					crypt_d.initialized = 0;
					int generate_idx = (int)pow(2, idx_one) + idx_two;
					strcpy(gecos_variants[generate_idx], gecos_variants[idx_two]);
					gecos_variants[generate_idx][idx_one] = toupper(gecos_variants[generate_idx][idx_one]);
					hash_pass = crypt_r(gecos_variants[generate_idx], pass_ext, &crypt_d);
					fprintf(hashlist, "%s\n", hash_pass);
					fprintf(plainlist, "%s\n", gecos_variants[generate_idx]);
				}
			}

			fclose(plainlist);
			fclose(hashlist);

		}

	}

}


/***********************************************************************
* Cached versions of the cracking functions
***********************************************************************/

// the cached version of the dictionary attack algorithm
int cached_cracker(user* user_entry, FILE* output_file, char* hashlist_path, char* plainlist_path, int verbose_flag) {

	FILE *hashlist = fopen(hashlist_path, "r");
	FILE *plainlist = fopen(plainlist_path, "r");

	int success_status = 0;

	char user_hash[PASS_TYPE_LEN+PASS_SALT_LEN+PASS_HASH_LEN+1];
	snprintf(user_hash, PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s$%s", user_entry->password_type, user_entry->password_salt, user_entry->password_hash);

	char buf_hash[PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1], buf_plain[DICT_ENTRY_LEN];

	if (hashlist != NULL && plainlist != NULL) {
		
		fseek(hashlist, 0, SEEK_SET);
		fseek(plainlist, 0, SEEK_SET);

		while (fgets(buf_hash, PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1, hashlist) && fgets(buf_plain, DICT_ENTRY_LEN, plainlist)) {


			if (buf_hash[strlen(buf_hash)-1] == '\n')
				buf_hash[strlen(buf_hash)-1] = '\0';
			if (buf_plain[strlen(buf_plain)-1] == '\n')
				buf_plain[strlen(buf_plain)-1] = '\0';

			if (!strcmp(buf_hash, user_hash)) {
				success_status = 1;
				fprintf(output_file, "%s:%s\n", user_entry->name, buf_plain);
				if (verbose_flag)
					display_cracked_user(user_entry, buf_plain);
				break;
			}

		}

	}

	fclose(hashlist);
	fclose(plainlist);

	return success_status;

}

// the cached version of the GECOS variants cracking algorithm
int cached_gecos_cracker(user* user_entry, char* hashlist_path, char* plainlist_path, FILE* output_file, int verbose_flag) {

	int success_status = 0;

	char gecos_field[GECOS_LEN], *gecos_inter;
	char *token, tokenized[DICT_ENTRY_LEN];

	strcpy(gecos_field, user_entry->gecos);
	gecos_inter = gecos_field;

	FILE *hashlist, *plainlist;

	char username_hashlist_path[MAX_PATH_LEN], username_plainlist_path[MAX_PATH_LEN];

	char user_ext[PASS_TYPE_LEN+PASS_SALT_LEN+1], user_hash[PASS_TYPE_LEN+PASS_SALT_LEN+PASS_HASH_LEN+1];
	snprintf(user_ext, PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s", user_entry->password_type, user_entry->password_salt);
	snprintf(user_hash, PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1, "$%s$%s$%s", user_entry->password_type, user_entry->password_salt, user_entry->password_hash);

	char buf_hash[PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1], buf_plain[DICT_ENTRY_LEN];

	while ((token = strtok_r(gecos_inter, GECOS_DELIM, &gecos_inter))) {

		strcpy(tokenized, token);
		for(int tok_idx = 0; tokenized[tok_idx] != '\0'; tok_idx++)
			tokenized[tok_idx] = tolower(tokenized[tok_idx]);
		
		snprintf(username_hashlist_path, MAX_PATH_LEN, "%s-%s", hashlist_path, tokenized);
		snprintf(username_plainlist_path, MAX_PATH_LEN, "%s-%s", plainlist_path, tokenized);
	
		hashlist = fopen(username_hashlist_path, "r");
		plainlist = fopen(username_plainlist_path, "r");

		while (fgets(buf_hash, PASS_HASH_LEN+PASS_SALT_LEN+PASS_TYPE_LEN+1, hashlist) && fgets(buf_plain, DICT_ENTRY_LEN, plainlist)) {

			if (buf_hash[strlen(buf_hash)-1] == '\n')
				buf_hash[strlen(buf_hash)-1] = '\0';
			if (buf_plain[strlen(buf_plain)-1] == '\n')
				buf_plain[strlen(buf_plain)-1] = '\0';			

			if (!strcmp(buf_hash, user_hash)) {
				success_status = 1;
				fprintf(output_file, "%s:%s\n", user_entry->name, buf_plain);
				if (verbose_flag)
					display_cracked_user(user_entry, buf_plain);
				break;
			}

		}

		fclose(hashlist);
		fclose(plainlist);

	}

	return success_status;

}
