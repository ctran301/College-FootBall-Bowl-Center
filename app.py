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
conn_string = f"{c.username}:{c.password}@127.0.0.1/football_db"
engine = create_engine(f'mysql://{conn_string}')


# reflect sqliteDB into a new model Base
Base = automap_base()
# reflect tables into Base
Base.prepare(engine, reflect=True)

# Assign table refference to a vars
BowlHistory = Base.classes.flsk_bowl_history
BowlOutcome = Base.classes.flsk_bowl_outcome
BowlPlayers = Base.classes.flsk_bowl_players

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
#Years dropdown menu
def yearsMenu():

    with engine.connect() as con:
        rs = con.execute('SELECT year FROM years_vw')
        for row in rs:
            years.append(row.year)
    return years

#Bowls dropdown menu
def bowlsMenu():
    
    with engine.connect() as con:
        rs = con.execute('SELECT bowl FROM bowls_vw')
        for row in rs:
            bowls.append(row.bowl)
    return bowls

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


#=====================
#Route to stats page
#=====================
@app.route("/stats")
def stats():
    yearsMenu()
    bowlsMenu()    
    return (
        render_template("stats.html", years=years, bowls=bowls)
    )

#======================
#Route to API Documentation Page
#======================
@app.route("/apiV1.0")
def api():
    return (
        render_template("api.html")
    )

#======================
#Route to Extraction Documentation Page
#======================
@app.route("/apiV1.0/extract")
def extract():
    return (
        render_template("extract.html")
    )


#======================
#Route to Tranformation Documentation Page
#======================
@app.route("/apiV1.0/transform")
def transform():
    return (
        render_template("transform.html")
    )

#======================
#Route to Load Documentation Page
#======================
@app.route("/apiV1.0/load")
def load():
    return (
        render_template("load.html")
    )

#======================
#Route to Extraction Documentation Page
#======================
@app.route("/apiV1.0/data")
def data():
    return (
        render_template("data.html")
    )

#======================
#Get route select team and get a table of all games/bowl appearances, opponent, game outcome
#======================
@app.route("/apiV1.0/outcome/<year>")
def game_record(year):

    results = (session.query(BowlOutcome.bowl, 
                             BowlOutcome.home_team, 
                             BowlOutcome.away_team, 
                             BowlOutcome.home_score, 
                             BowlOutcome.away_score, 
                             BowlOutcome.winning_team,
                             BowlOutcome.loosing_team)
                .filter(BowlOutcome.year == year)
                .order_by(BowlOutcome.bowl)
                .all())
    
    return jsonify(results) 

#=====================
#Get route returns list of all bowl games, year, team1, team2, winner
#=====================
@app.route("/apiV1.0/history")
def history():

    results = (session.query(BowlHistory.bowl, 
                             BowlHistory.cnt_games, 
                             BowlHistory.min_year, 
                             BowlHistory.max_year, 
                             BowlHistory.home_teams, 
                             BowlHistory.away_teams)
                .order_by(BowlHistory.bowl)                             
                .all())
    
    return jsonify(results) 

#=====================
#Get route returns players who played in a specific bowl game and specific year
#=====================
@app.route("/apiV1.0/roster/<bowl>/<year>")
def players(bowl,year):

    results = (session.query(BowlPlayers.team, 
                             BowlPlayers.player)
                .filter(BowlPlayers.year == year)
                .filter(BowlPlayers.bowl == bowl)                
                .order_by(BowlPlayers.team, BowlPlayers.player)
                .all())
    
    if (len(results) > 0):
        return jsonify(results) 
    else:
        return "There is no " + bowl + " data for " + year + "."

if __name__ == '__main__':
    app.run(debug=True)

#Start app commands
# $ python app.py
#      or
#$ export FLASK_APP=app.py
#$ flask run

#App runs on local host (http://127.0.0.1:5000/)
