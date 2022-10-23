# Pokeset

## About

Pokeset is a web application that allows for easy recording and querying of
custom Pokemon. Randomizers are popular game modifications wherein various
elements of a game that were previously static are made random. This app
is intended to be used for storing information from a playthrough of a
randomized Pokemon game. Where the in-game Pokedex breaks down, Pokeset
picks up the slack!

This app is our capstone project for COMP30022.

## Team

* Gurjeet Cheema: Scrum Master & Backend/Frontend

* James Amanatidis: Backend Lead
	
* Thomas Black: Product Owner & Backend
	
* Felix Esperson: Frontend Lead
	
* Nicholas Lim: Client Liaison & Frontend

## Set-up

Follow these steps to run this repository locally:

1. Install [Python](https://www.python.org/downloads/) 
2. Install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/), following the [instructions](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) for your operating system.
3. Install [mysqlclient](https://pypi.org/project/mysqlclient/) using [pip](https://pypi.org/).
4. Install [Django](https://docs.djangoproject.com/en/4.1/intro/install/) using pip.
5. Log into MySQL and create a new database called "pokeset_db", like so:
```
mysql -u 'YOUR_USERNAME' -p
CREATE DATABASE pokeset_db;
```
6. Under the project folder "pokeset", create a file named "my.cnf" with this text with "YOUR_USERNAME" and "YOUR_PASSWORD" replaced appropiately:
```
[client]
database = pokeset_db
host = localhost
user = YOUR_USERNAME
password = YOUR_PASSWORD
default-character-set = utf8
```
7. You should now be able to run the server with ```python3 manage.py runserver```. Don't forget to migrate (```python3 manage.py migrate```).
