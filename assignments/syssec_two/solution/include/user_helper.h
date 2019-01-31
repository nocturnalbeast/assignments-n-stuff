/***********************************************************************
* FILENAME : user_helper.h
*
* DESCRIPTION :
*       This header file contains the data structure used to 
*       represent a user and store its data that's been extracted.
*       It also contains some helper functions to perform
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
* User parameters
***********************************************************************/

// maximum length of a username
#define NAME_LEN 100
// maximum length of the GECOS field
#define GECOS_LEN 200
// maximum length of the home directory
#define HOME_LEN 100
// maximum length of the path to the shell used
#define SHELL_LEN 100
// maximum length of the password hash
#define PASS_HASH_LEN 200
// maximum length of the salt used in hashing
#define PASS_SALT_LEN 50
// maximum length of the field that specifies the type of the password
// hash
#define PASS_TYPE_LEN 10


/***********************************************************************
* Basic structure definitions
***********************************************************************/

typedef struct user {
	char name[NAME_LEN], gecos[GECOS_LEN], home[HOME_LEN], shell[SHELL_LEN];
	int uid, gid;
	char password_hash[PASS_HASH_LEN], password_salt[PASS_SALT_LEN], password_type[PASS_TYPE_LEN];
} user;


/***********************************************************************
* Helper functions
***********************************************************************/

// function to generate a struct object, not really used
user* generate_user(char* user_name, char* full_name, char* home_dir, char* shell, int uid, int gid, char* pass_type, char* pass_hash, char* pass_salt) {

	user* new_user = (user*)malloc(sizeof(user));

	strcpy(new_user->name, user_name);
	strcpy(new_user->gecos, full_name);
	strcpy(new_user->home, home_dir);
	strcpy(new_user->shell, shell);
	new_user->uid = uid;
	new_user->gid = gid;
	strcpy(new_user->password_hash, pass_hash);
	strcpy(new_user->password_type, pass_type);
	strcpy(new_user->password_hash, pass_salt);

	return new_user;

}

// function to update the given user with the details provided
int update_user(user* curr_user, char* user_name, char* full_name, char* home_dir, char* shell, int uid, int gid, char* pass_type, char* pass_hash, char* pass_salt) {

	strcpy(curr_user->name, user_name);
	strcpy(curr_user->gecos, full_name);
	strcpy(curr_user->home, home_dir);
	strcpy(curr_user->shell, shell);
	curr_user->uid = uid;
	curr_user->gid = gid;
	strcpy(curr_user->password_hash, pass_hash);
	strcpy(curr_user->password_type, pass_type);
	strcpy(curr_user->password_hash, pass_salt);

	return 0;

}

// function to update the given user with the details provided, but only
// those extracted from the passwd file
int update_user_passwd(user* curr_user, char* user_name, char* full_name, char* home_dir, char* shell, int uid, int gid) {

	strcpy(curr_user->name, user_name);
	strcpy(curr_user->gecos, full_name);
	strcpy(curr_user->home, home_dir);
	strcpy(curr_user->shell, shell);
	curr_user->uid = uid;
	curr_user->gid = gid;

	return 0;

}

// function to update the given user with the details provided, but only
// those extracted from the shadow file
int update_user_shadow(user* curr_user, char* pass_type, char* pass_hash, char* pass_salt) {

	strcpy(curr_user->password_hash, pass_hash);
	strcpy(curr_user->password_type, pass_type);
	strcpy(curr_user->password_salt, pass_salt);

	return 0;

}

// simple wrapper for realloc to resize the dynamically allocated list
user* resize_list(user* user_list, int size) {

	user* list_resized = (user*)realloc(user_list, size * sizeof(user));
	return list_resized;

}