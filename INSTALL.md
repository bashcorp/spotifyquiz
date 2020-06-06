# spotifyquiz
Spotify Quiz!

# Setting up the Server
## Virtual Environments

### Installing
A virtual environment is a way to install software into a folder in your project, so it doesn't install for the whole computer. So if you have a bunch of different projects with different software version requirements, this is an easy way of managing it.
Django hasn't supported python 2 for a while, so you should probably install python 3.
Once you do, go to the root folder of your project and run `python3 -m venv venv_folder`
*(Note: You may need to install other python libraries, I can't remember. Follow the any instructions given to you)*

### Using
To use commands with the software installed in the virtual environment, run `source venv_folder/bin/activate` You can use the terminal like usual, but commands from programs in the virtual environment will use that software.

### Installing software with pip
Pip is python's package manager. To install a program, you'd run `pip install program`. (To install into the virtual environment, make sure you've run the activate script)
If you have a bunch of programs installed, you can save the list of programs to a text file by running `pip freeze > requirements.txt`. You can then install all the programs in such a list by running `pip install -r requirements.txt`.

I've included a `requirements.txt` in the github repository, so you should install from that.


# Starting the Server
`source` into your virtual environment and then run `python manage.py runserver`. This will start the server, which will be on localhost:8000
