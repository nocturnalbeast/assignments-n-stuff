# use debian, recommended for server setups
# using stretch (9) here
FROM debian:stretch

# use tini for proper (and safer) process handling
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# use noninteractive mode while installing
ENV DEBIAN_FRONTEND noninteractive

# push the provisioning script provided alongside this file into the container
COPY ./dsquared-server-setup.sh /root/setup.sh
# and make it executable
RUN chmod +x /root/setup.sh
# provision the server using the setup script pushed into the container
RUN /root/setup.sh
# then remove the provisioning script
RUN rm /root/setup.sh

# copy the website into the server directory 
COPY ./website /var/www/html
# repair access control for website
RUN chown www-data:www-data /var/www/html/ -R

# copy the startup script into the container
COPY ./web-server-start.sh /root/start.sh
# and make it executable
RUN chmod +x /root/start.sh

# switch back to teletype after package installation
ENV DEBIAN_FRONTEND teletype

# set the working directory to the server directory
# not required, but recommended
WORKDIR /var/www/html

# finally start the server on boot and get an interactive shell
CMD ["/root/start.sh"]

# Make port 80 available to the world outside this container
EXPOSE 80/tcp