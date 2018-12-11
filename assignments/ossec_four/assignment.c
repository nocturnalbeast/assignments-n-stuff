//proc_fs assignment code.

#include <linux/module.h>		// all kernel modules need this.
#include <linux/kernel.h>		// needed for printk and its modes.
#include <linux/init.h>			// needed for init functions.
#include <linux/uaccess.h>		// needed for copy_from_user.
#include <linux/proc_fs.h>		// needed for proc file management, the struct and so on.

#define BUF_SIZ 1024			// setting the max buffer size for the proc file.
#define DEV_NAME "xorencdev"	// the name of the proc file.
#define XOR_KEY 13				// the key value for xor cipher operations.

MODULE_DESCRIPTION("ossec-four assignment module");	// short description of the module.
MODULE_AUTHOR("nocturnalbeast");					// author of the module.
MODULE_LICENSE("GPL");								// license that the module's code is published under.

// Declaring the proc_dir_entry file that is the pointer to the file
// which is going to be created in the /proc directory.
static struct proc_dir_entry *proc_file;

// Declaring the proc file buffer, which will hold the data from the
// proc file.
static char character_buffer[BUF_SIZ];

// Declaring the buffer's variable data size, which is to be
// used in the read and write operations.
static unsigned long buffer_size = 0;

// The write-to-file operation, in which the proc file is written to
// with the character buffer.
static ssize_t procfile_write(struct file *file,const char *buffer, size_t count, loff_t *offset)
{
	buffer_size = count;
	if (buffer_size > BUF_SIZ) {
		buffer_size = BUF_SIZ;
	}
	if (copy_from_user(character_buffer, buffer, buffer_size)) {
		return -EFAULT;
	}
	return buffer_size;
}

// The read-from-file operation, in which the data from the buffer is
// read from and displayed to the user.
// It is also to be noted that the XOR cipher operation and hex
// representation conversion is performed here.
static ssize_t procfile_read(struct file *file, char *buffer, size_t buffer_length, loff_t *offset)
{
	static long int i = 0;
	static int flag = 0;
	if (flag) {
		printk(KERN_INFO "Empty file!\n");
		flag = 0;
		return 0;
	}
	flag = 1;
	printk(KERN_INFO "Reading from proc_file:\n");
	for(i = 0; character_buffer[i] != '\0'; i++)
		sprintf(buffer+i*2, "%02X", character_buffer[i] ^ XOR_KEY);
	return (i-1)*2;
}

// The file_operations structure that describes what operations can be
// done, and references those operations to the resepctive functions
// that handle those operations.
static struct file_operations fops_struct = {
	.read = procfile_read,
	.write = procfile_write,
};

// Inititalization function that creates the proc file and links it
// to the file_operations structure created earlier. Also handles
// no memory issues with checking with pointer for null values.
static int __init assignment_init(void)
{
	proc_file = proc_create(DEV_NAME, 0666, NULL, &fops_struct);
	if (proc_file == NULL) {
		remove_proc_entry(DEV_NAME, NULL);
		printk(KERN_ALERT "Error in creating proc_file!\n");
		return -ENOMEM;
	}
	printk(KERN_INFO "proc_file successfully created!\n");
	return 0;
}

// Cleanup function that removes the proc file from the /proc
// directory, and informs the user about it.
static void __exit assignment_exit(void)
{
	remove_proc_entry(DEV_NAME, NULL);
	printk(KERN_INFO "proc_file removed!\n");
}

// Mapping the module initialization function and the 
// module termination function to the functions discussed
// earlier.
module_init(assignment_init);
module_exit(assignment_exit);
