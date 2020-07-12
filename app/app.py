from module.functions import find_tution_cost, prepare_chart_data, get_state_wage
from static.data.processed.Classification import Classify
import os
import json
from flask import Flask, request, render_template, url_for, redirect, jsonify

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

from bson.json_util import dumps

# Create an instance of our Flask app.
app = Flask(__name__, static_url_path="/static")

# Create connection variable
conn = "mongodb://localhost:27017"

# Pass connection to the pymongo instance.
dbconn = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = dbconn.FortunEd

majors = db.Majors
coli = db.LivingCost
university = db.Universities.find()
university_data = list(university)
job_majors = db.Majors
state_wages = db.StateWage

# Define routes
@app.route("/")
def welcome():
    return render_template("login.html")

# render a login route
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        #password = request.form["password"]
        if request.form["radProfile"] == "1":
            profile = "High school Student"
        elif request.form["radProfile"] == "2":
            profile = "College Student"
        elif request.form["radProfile"] == "1":
            profile = "Parent / Advisor"
        else:
            profile = "Browser"
        if request.form["cbOptIn"] == "on":
            option = "opted in"
        else:
            option = "opted out"

        message = '<h4> The responses were ' + username + \
            ', ' + profile + ', ' + option + '</h4>'

        return render_template("index.html", message=message)

    return render_template("register.html")
# render a login route
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/results")
def results():
    majors_data = majors.find_one()
    return render_template("results.html", master_major_data=majors_data)


@app.route("/csoptions")
def collect_cs_params():
    return render_template("cs-search-params.html")


@app.route("/parents")
def parents_data():
    return render_template("parents.html")

    # return render_template("cs-search-params.html")


@app.route("/csresults", methods=["POST", "GET"])
def show_cs_results():

    if request.method == "POST":
        state = request.form["state"]
        major = request.form["major"]
        loan = request.form["loan"]

    # get the state we are interested in based on state parameter
    data_living_wage = get_state_wage(state, state_wages)
    print(data_living_wage)
    print(state)
    print(major)
    print(loan)

    outcome = Classify(state, major, loan)
    # print(outcome.keys())
    # print(outcome)
    # store data as a dictionary
    #state_wages_dict = data[0]

    coli_data = coli.find_one({"State": state})
    jm_data = job_majors.find({"Major_Category": major})
    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)

    return render_template("cs-search-results.html",  coli_data=coli_data, job_majors=job_majors_list)


@app.route("/hsoptions")
def collect_hs_params():
    return render_template("hs-search-params.html")


@app.route("/hsresults",  methods=["POST", "GET"])
def show_hs_results():

    # capture parameters / user options
    if request.method == "POST":
        state = request.form["state"]
        io_state = request.form["io_state"]
        major = request.form["major"]
        timing_pref = request.form["timing"]
        # if the user chose < 1 Year set timing to 1
        if request.form["timing"] == "Less than 1 Year":
            timing = 1

        # else set timing to 2
        else:
            timing = 2

    # track preferences for in-state vs out-of-state and timing for going to college
    pref = {}
    pref.update({"in_vs_out": io_state, "timing": timing_pref})

    print(state)
    print(io_state)
    print(major)
    print(timing)

    tuition_data = find_tution_cost(state, timing, university_data)
    print(tuition_data)

    university_cost_data = prepare_chart_data('university', university_data)
    print(university_cost_data)

    coli_data = coli.find_one({"State": state})

    jm_data = job_majors.find({"Major_Category": major})

    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)
    # print(job_majors_list[0]["Majors"])
    return render_template("hs-search-results.html",  tuition_data=tuition_data, university_cost_data=university_cost_data, pref=pref)


# @app.route("/guardian.html")
# def guardian():
#     return render_template("guardian.html")

# # @app.route("/results.html/<state>, <in_out>,<major>,<timeframe>")
# # def HS_Visualization(major):
# #     cost_data = db.cost_analysis.find_one({"major": f"{major}", "state"})
# #     income_data = db.income_analysis.find_one({"major": f"{major}"})
# #     options_data = db.options_analysis.find_one({"major": f"{major}"})
# #     outlook_data = db.outlook_analysis.find_one({"major": f"{major}"})
# #     predict_data = db.outlook_analysis.find_one({"major": f"{major}"})
if __name__ == "__main__":
    app.run(debug=True)
