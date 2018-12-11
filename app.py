import numpy as np
import pandas as pd
import logging
import sqlalchemy
import datetime as dt
import sys
sys.path.append("static/assets/Resources/")
import config as c
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData
from sqlalchemy.pool import StaticPool
from flask import Flask, jsonify, render_template



logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

#=======================
#    Database Connection
#=======================
conn_string = f"{c.userName}:{c.passW}@127.0.0.1/football_db"
engine = create_engine(f'mysql://{conn_string}')


# reflect sqliteDB into a new model Base
Base = automap_base()
# reflect tables into Base
Base.prepare(engine, reflect=True)

# Assign table refference to a vars
Player = Base.classes.player_stats
Game = Base.classes.game_stats

# Create Session obj
session = Session(engine)

#========================
#    Initialize Flask app
#========================
app = Flask(__name__)


#=========================
#                Functions
#=========================
#global varriables
teams = {}
bowls = {}
years = {} #2007-2016


#=========================
#Create Dropdown arrays
#=========================
#Teams dropdown menu
def teamsMenu():
    
    return(

    )

#Bowls dropdown menu
def bowlsMenu():
    
    return(

    )

#========================
#          Publish Routes
#========================


#======================
#Root Get Route
#======================
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        render_template("index.html")
    )

#======================
#Get route select team and get a table of all games/bowl appearances, opponent, game outcome
#======================
@app.route("/apiV1.0/<team>")
def team_record(team):

    return (
        "Team Game Record:</br>"+
        "Select a team and see all bowl game appearences, opponents, game outcome."
    )

#=====================
#Get route returns list of all bowl games, year, team1, team2, winner
#=====================
@app.route("/apiV1.0/history")
def history():

    return (
        "Bowl Game History:</br>"+
        "Returns list of all bowl games, year, team1, team2, & winner"
    )

#=====================
#Get route returns players who played in a specific bowl game and specific year
#=====================
@app.route("/apiV1.0/<bowl>/<year>")
def players(bowl,year):

    return (
        "Bowl team roster (by year):"+
        "User selects a bowl game and a year from drop downs."+
        "Returns a player roster who played in a specific bowl game and specific year."
    )

if __name__ == '__main__':
    app.run(debug=True)

#Start app commands
# $ python app.py
#      or
#$ export FLASK_APP=app.py
#$ flask run

#App runs on local host (http://127.0.0.1:5000/)