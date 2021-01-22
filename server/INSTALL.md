# SpotOn Server-Side

# Setting up the Server
This guide fully describes how to set up the server on your local machine.
It's meant for someone who doesn't have experience with server-side technologies.

## Server Dependencies & Virtual Environments

### Installing
A virtual environment is a way to install software for only your project,
instead of your entire computer. This way, if you have several different
projects that use different versions of the same software, you can manage that
easily. 

Make sure you have python3 installed. Then go to the server/ folder of the
project and run `python3 -m venv venv_folder` (you can use any name for the
venv_folder. I just use 'venv').

### Using
In the terminal, to use commands from software in the virtual environment, you
must run `source venv_folder/bin/activate`. Now, normal commands will still
work, but any commands associated with virtual environment programs will use
those programs.

You'll need to activate your virtual environment to install server-side
dependencies, run the server, and run the tests.

### Installing Server Dependencies
pip3 is python's package manager. To install all the server dependencies, go
to the server/ folder, activate the virtual environment, and run
`pip3 install -r requirements.txt`.


## Database

### Installing
The server uses MySQL as its database. You'll need to install that however you
do on your system.

### Setup
You'll need to create the server's database and grant the proper priveleges.

To create the database, from inside of MySQL, run `CREATE DATABASE spoton;`

You'll need to give the server's user permissions to access this database.
Run `GRANT ALL PRIVILEGES ON spoton.* TO 'spoton'@'localhost';`

### Migrating the Server's Changes
To create the proper tables in the database, from the server/ folder and with
the virtual environment activated, run `python3 manage.py migrate`.


# Testing the Server
The best way to make sure that everything is working properly is to run the 
server's tests. To do this, from the server/, with the virtual environment
activated, run `python3 manage.py test -v2` (the `-v2` is not necessary, but it
makes the tests look cooler).


# Starting the Server
If the tests all pass, then you're good to run the server! From the same place,
run `python3 manage.py runserver`. This will start the server locally on port
8000.
