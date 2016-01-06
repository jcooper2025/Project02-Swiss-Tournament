# Project02-Swiss-Tournament
Repository for the Swiss Tournament Project as part of the Udacity Fullstack Nanodegree

This repository containa the files necessary to run the Second Project as part of the Udacity Full Stack Nanodegree. This is a small database to track a multiround swiss tournament.

A full explaination of the logic for the Swiss Pairing tournament can be found here:
	https://en.wikipedia.org/wiki/Swiss-system_tournament

Prerequisites/Assumptions:
1) Vagrant is installed locally and the Full Stack Nanodegree VM is running with the SQL stack. Instructions for setting this up are here:
	https://discussions.udacity.com/t/vagrant-virtual-machines-and-the-udacity-development-environment/15924

2) After the Vagrant environment is up and running, download the repository zip file to your local machine by clicking the zip button on this page:


3) Next unzip the file and copy over the python and sql files to the common directory for your virtual machine.


Steps to execute:
1) Open a terminal window and change to the common directory for your virtual machine. The same directory where you copied the python and sql files.

2) Start the Virtual machine and log into it with the commands:
	$ vagrant up
	$ vagrant ssh

3) After logging into the vagrant machine change to the directory common with your host machine where you copied the python and sql files.

4) Start the pqsl engine and run the sql file using the commands:
    $pqsl
    psql=>\i filename.sql

5) Open a second terminal window and move to the same directory from Step 1.

6) In the new window log into the vagrant machine and change too the common directory from steps 2 and 3.

7) From the command line, execute the python test script:
    $python filename.py

