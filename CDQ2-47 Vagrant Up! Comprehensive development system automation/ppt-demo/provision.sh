#!/bin/bash

# =======================================================================
# update yum and install some useful tools 
# =======================================================================
sudo yum update -y --exclude=kernel
sudo yum install -y vim git unzip screen wget expect

# =======================================================================
# APACHE
# install apache service and allow if to start up everytime the box is 
# turned on (OFF -> ON). Then stop the apache service and continue to
# configure our box!
# =======================================================================
sudo yum install -y httpd httpd-devl httpd-tools
sudo systemctl enable httpd.service
sudo systemctl stop httpd.service

# =======================================================================
# Disable SELINUX so we dont get a "forbidden" error when accessing the
# localhost. To disbale SELINUX we need to specify this inside the config file
# located at '/etc/selinux/config. This sed command is used to 
# replace 'SELINUX=enforcing' with 'SELINUX=disabled' in the file '/etc/selinux/config'
# =======================================================================
sudo sed -i -e 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# =======================================================================
# We also need to configure Apache so it doesnt not display the default
# 'welcome page'. Do do this we need to comment out every line inside the 
# file located at '/etc/httpd/conf.d/welcome.conf'. This sed commmand
# comments out everyline that is NOT already commented.
# =======================================================================
sudo sed -i -e 's/^#*/#/' /etc/httpd/conf.d/welcome.conf

# =======================================================================
# Create a symbolic link for our shared folder between the host and the
# guest machine ("/vagrant" folder). Link our shared folder to 
# the "/var/www/html" folder which is what Apache is configured to serve.
# Then we start the Apache service!
# =======================================================================
sudo rm -rf /var/www/html
ln -s /vagrant /var/www/html
sudo systemctl start httpd.service

# =======================================================================
# PHP
# install PHP 
# =======================================================================
sudo yum install -y php php-cli php-common php-devel php-mysql


# =======================================================================
# Download our index.html and info.php files for Apache to display.
# We download these files inside of our shared folder.
# =======================================================================
cd /vagrant
sudo -u vagrant wget -q https://raw.githubusercontent.com/nickb210/Vagrant/master/files/index.html
sudo -u vagrant wget -q https://raw.githubusercontent.com/nickb210/Vagrant/master/files/info.php

sudo systemctl restart httpd.service