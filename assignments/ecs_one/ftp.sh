#!/bin/sh
HOST='ftp.yoursite.com'
USER='username'
PASSWD='password'
FILE='*.zip'

ftp -in $HOST <quote USER $USER
quote PASS $PASSWD
cd www
binary
put $FILE
quit
END_SCRIPT
exit 0
