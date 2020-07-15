from module.functions import *
# find_tution_cost, prepare_chart_data, get_state_wage, get_job_specs, four_year_cost, bestIncomeStates, whaterfall, get_top_5_majors_list,get_top_5_states_for_loan_repay
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
    return render_template("index.html")

@app.route("/csoptions")
def collect_cs_params():
    return render_template("cs-search-params.html")


@app.route("/parents")
def parents_data():
    return render_template("parents.html")

@app.route("/csresults", methods=["POST", "GET"])
def show_cs_results():
    if request.method == "POST":
        state = request.form["state"]
        major = request.form["major"]
        loan = request.form["loan"]
        

    # get the state we are interested in based on state parameter
    data_living_wage = get_state_wage(state, state_wages)
    # print(data_living_wage)
    # print(state)
    # print(major)
    # print(loan)

    whaterfall_data = whaterfall(db, state, major, loan)
    best_majors = get_top_5_majors_list(db, major)
    best_states = get_top_5_states_for_loan_repay(db, major, loan)
    pay_off_options = get_pay_off_period_variation(db, state, major, loan)
    # print(pay_off_options['Percentages'])

    outcome = Classify(state, major, loan)
    # print(outcome.keys())
    # print(outcome)
    # store data as a dictionary
    #state_wages_dict = data[0]

    coli_data = coli.find_one({"State": state})
    # print(coli_data)
    jm_data = job_majors.find({"Major_Category": major})
    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)

    return render_template("cs-search-results.html",  coli_data=coli_data, job_majors=job_majors_list, whaterfall_data=whaterfall_data,
    best_majors=best_majors, best_states=best_states, pay_off_options=pay_off_options, outcome=outcome, major=major)


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

    # print(state)
    # print(io_state)
    # print(major)
    # print(timing)

    job_specs = get_job_specs(db, major)
    # print(job_specs)
    top_states = bestIncomeStates(db, major)
    dict_ = four_year_cost(db, state, io_state, timing)
    state_wage_data = get_state_wage(state, state_wages)
    median_income_majors = get_median_income_by_majors(db, major)
    # print(state_wage_data)
    print(median_income_majors)

    tuition_data = find_tution_cost(state, timing, university_data)
    # print(tuition_data)

    university_cost_data = prepare_chart_data('university', university_data)
    # print(university_cost_data)
    
    state_college_cost_over_time = state_uni_cost_over_time(university_data, state)
    # print(state_college_cost_over_time)

    coli_data = coli.find_one({"State": state})

    jm_data = job_majors.find({"Major_Category": major})

    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)
    # print(job_majors_list[0]["Majors"])
    return render_template("hs-search-results.html",  tuition_data=tuition_data, university_cost_data=university_cost_data, pref=pref,
                                                        job_specs=job_specs, top_states=top_states, dict_=dict_, io_state=io_state,
                                                        major=major, median_income_majors=median_income_majors, state_college_cost_over_time=state_college_cost_over_time)


@app.route("/team")
def team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)
