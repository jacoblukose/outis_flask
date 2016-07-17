#docs falls here

FLASK PACKAGE
==============

This package implements a visualization plugin for Elasticsearch, where user can analyse content indexed on top of an Elasticsearch cluster. 

SETUP
=====

 1. Install Elasticsearch 2.3.3 and Java 8 

 	-----------------------------------------------
 	Add the Oracle Java PPA to apt:

	sudo add-apt-repository -y ppa:webupd8team/java
	
	Update your apt package database:

	sudo apt-get update
	
	Install the latest stable version of Oracle Java 8 with this command (and accept the license agreement that pops up):

	sudo apt-get -y install oracle-java8-installer
	
	Lastly, verify it is installed:

	java -version
	-------------------------------------------------
	You can download the tar file from www.elastic.co  

	Extract and start the service as bin/elasticsearch
	--------------------------------------------------


 3. pip install the  packages from requirement.txt:

 		pip install -r requirements.txt


 4. To run,
    python esflask.py


 5. Point your web browser at the server at

    http://localhost:5000/

    to begin.

ABOUT THE CODE
==============

The code provides a tool for users to perform data analysis upon data 
indexed on elasticsearch cluster. It allow allows users to perform serch 
operation on queries under various formats which can be followed on 
"https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax" 

If you aren't familiar with the flask web framework, you can quickly
start looking at the important code by looking in the flask file:

Each function is a python callable that responds to an HTTP request.



 

