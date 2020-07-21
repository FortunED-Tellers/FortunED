from module.functions import *
from module.backend import transfer_data
from static.data.processed.Classification import Classify
import datetime
import os
import json
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, url_for, redirect, jsonify
import pymongo
from bson.json_util import dumps

# Create an instance of our Flask app.
app = Flask(__name__, static_url_path="/static")

# Create connection variable
conn = "mongodb+srv://fort_user:TCU7sGNl3Y3OyEnM@cluster0.wv5gd.mongodb.net/fortuned?retryWrites=true&w=majority"

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

# generate DataFrame to track metrics for KPI
KPI = pd.DataFrame(columns=["Student ID", "Student Type", "State", "In-Out State", "Area of Study", "Time to College", "Loan", "Time of Access"]).set_index("Student ID")
cntr = 1

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

        # set values for the audit metrics table    
        student_type = "College"
        io_state = None
        time_to_college = None
        time_of_access = datetime.datetime.now()
        
        
        # set the data as as a list array for loading dataframe based on position
        metrics=[None, student_type,state, io_state, major,time_to_college, loan, time_of_access]
        
        #Populate the metrics 
        KPI.append(metrics, ignore_index=True)
        

        # Call function to transfer data for tableau reporting
        #transfer_data("KPIs.xlsx", "YTD_Status", metrics) 

    

    # ++++++++++++++++++++++++++++++++++++++++++++
    # CALL FUNCTIONS TO RETURN DATA FOR  TEMPLATES
    # ++++++++++++++++++++++++++++++++++++++++++++

    data_living_wage = get_state_wage(state, state_wages)
    whaterfall_data = whaterfall(db, state, major, loan)
    best_majors = get_top_5_majors_list(db, major)
    best_states = get_top_5_states_for_loan_repay(db, major, loan)
    pay_off_options = get_pay_off_period_variation(db, state, major, loan)
    outcome = Classify(state, major, loan)
    coli_data = coli.find_one({"State": state})
    jm_data = job_majors.find({"Major_Category": major})
    job_majors_list = []

    for record in jm_data:
        job_majors_list.append(record)

    # ++++++++++++++++++++++++++++++++++++++++++++
    # RENDER THE College Student Results TEMPLATE
    # ++++++++++++++++++++++++++++++++++++++++++++
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

        # set values for the audit metrics table    
        student_type = "High School"
        loan = None
        time_to_college = timing_pref
        time_of_access = datetime.datetime.now()
        io_state_metric = io_state
        if len(io_state_metric) == 0:
            io_state_metric = "in"
        elif io_state_metric == "in-state":
            io_state_metric = "in"
        elif io_state_metric == "out-of-state":
            io_state_metric = "out"
        
        # set the data as as a list array for loading dataframe based on position
        metrics=[None, student_type,state, io_state_metric, major,time_to_college, loan, time_of_access]
        
        
        # Populate the metrics 
        KPI.append(metrics, ignore_index=True)

        # Call function to transfer data for tableau reporting
        #transfer_data("KPIs.xlsx", "YTD_Status", metrics)

        # track preferences for in-state vs out-of-state and timing for going to college
        pref = {}
        pref.update({"in_vs_out": io_state, "timing": timing_pref})

    # ++++++++++++++++++++++++++++++++++++++++++++
    # CALL FUNCTIONS TO RETURN DATA FOR  TEMPLATES
    # ++++++++++++++++++++++++++++++++++++++++++++

    job_specs = get_job_specs(db, major)

    top_states = bestIncomeStates(db, major)

    dict_ = four_year_cost(db, state, io_state, timing)

    state_wage_data = get_state_wage(state, state_wages)

    median_income_majors = get_median_income_by_majors(db, major)

    tuition_data = find_tution_cost(state, timing, university_data)

    university_cost_data = prepare_chart_data('university', university_data)
    
    state_college_cost_over_time = state_uni_cost_over_time(university_data, state)
  

    coli_data = coli.find_one({"State": state})

    jm_data = job_majors.find({"Major_Category": major})

    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)
   
    # ++++++++++++++++++++++++++++++++++++++++++++
    # RENDER THE High School Results TEMPLATE
    # ++++++++++++++++++++++++++++++++++++++++++++
    return render_template("hs-search-results.html",  tuition_data=tuition_data, university_cost_data=university_cost_data, pref=pref,
                                                        job_specs=job_specs, top_states=top_states, dict_=dict_, io_state=io_state,
                                                        major=major, median_income_majors=median_income_majors, state_college_cost_over_time=state_college_cost_over_time)


@app.route("/team")
def team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)
