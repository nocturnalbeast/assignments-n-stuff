#!/bin/bash

# clean apt cruft (just in case)
apt-get autoclean
apt-get autoremove
# update package lists
apt-get update

# install apt-utils for package configuration
apt-get install -y --no-install-recommends apt-utils
# setup apt to work correctly with https sources
apt-get install -y --no-install-recommends apt-transport-https ca-certificates
# install support for adding other repositories via the add-apt-repository command
apt-get install -y --no-install-recommends software-properties-common

# then upgrade all packages
apt-get dist-upgrade -y --no-install-recommends -o Dpkg::Options::="--force-confold"

# install apache webserver
# doesn't need apache2-utils explicitly mentioned
apt-get install -y apache2
# get apache webserver to start on boot
update-rc.d apache2 defaults
# start apache webserver
service apache2 start

# create server directory if it doesn't exist
mkdir -p /var/www/html
# change ownership to apache user
chown www-data:www-data /var/www/html/ -R

# install mariadb database server
apt-get install -y mariadb-server mariadb-client
# get database server to start on boot
update-rc.d mysql defaults
# start database server
service mysql start

# taken from https://stackoverflow.com/questions/24270733/automate-mysql-secure-installation-with-echo-command-via-a-shell-script#27759061
# make sure that NOBODY can access the server without a password
mysql -e "UPDATE mysql.user SET Password = PASSWORD('root') WHERE User = 'root'"
# kill the anonymous users
mysql -e "DROP USER ''@'localhost'"
# because our hostname varies we'll use some Bash magic here.
mysql -e "DROP USER ''@'$(hostname)'"
# kill off the demo database
mysql -e "DROP DATABASE test"
# make our changes take effect
mysql -e "FLUSH PRIVILEGES"

# install php, guess it's a transitional package, so dependencies will be handled fine
apt-get install -y php

# enable php in the apache installation
a2enmod php7.0
# and then restart the webserver to apply the changes
service apache2 restart
