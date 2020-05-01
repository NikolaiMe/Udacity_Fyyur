import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# IMPLEMENT DATABASE URL 
SQLALCHEMY_DATABASE_URI = 'postgres://nikol:hallo@localhost:5432/fyyur'
#--> As there doesn't seem to be a possibility to use psql without password on a Windows machine, I added a user 'nikol' with pw 'hallo' 
SQLALCHEMY_TRACK_MODIFICATIONS = False
