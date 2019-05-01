#!/usr/bin/python2

import subprocess

lst_chars = [ord(' ') for i in xrange(10)]

while lst_chars[0] != 128:
	brute_str = ''.join([chr(ele) for ele in lst_chars])
	proc_out = subprocess.Popen(["./vuln-prog"],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE)
	proc_ans = proc_out.communicate(brute_str)
	proc_ans = proc_ans[0][15:-1]
	if proc_ans == "You win!":
		print "Password found!\nIt is " + brute_str
		break
	lst_chars = [ele + 1 for ele in lst_chars]
