import os
import json
from flask import Flask, request, render_template, jsonify

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

from bson.json_util import dumps

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
dbconn = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = dbconn.fortunedb


# Define routes
@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/team.html")
def team():
    return render_template('team.html')

@app.route("/results.html/<county>")
def results():
    return render_template('results.html', array=array)

if __name__ == '__main__':
    app.run(debug=True)
