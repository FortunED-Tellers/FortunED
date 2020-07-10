import os
import json
from flask import Flask, request, render_template, url_for, redirect, jsonify

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

from bson.json_util import dumps

# Create an instance of our Flask app.
app = Flask(__name__,static_url_path="/static")

# Create connection variable
conn = "mongodb://localhost:27017"

# Pass connection to the pymongo instance.
dbconn = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = dbconn.FortunEd

majors = db.Majors
coli = db.LivingCost
university = db.Universities
job_majors = db.Majors

# university data
# # print(type(state_wages))
# state_wage_list = []
# state_wage_list = list(state_wages.find())
# result_values = [i["Alabama"]
#                  for i in state_wage_list[0]["data"] if "Alabama" in i]
# print(type(result_values))
# print(result_values)
# # create a dict to hold the major options which are currently stored as keys
# options = {}
# # get the list of keys from the list of dictionaries
# options = {k for d in result_values for k in d.keys()}
# print(options)
# # printing the actual values major or key, these will be parametized on the templates
# print(result_values[0]["living wage"])
# print(result_values[0]["Management"])


# options.update({})


# Define routes
@app.route("/")
def welcome():
    return render_template("index.html")


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


@app.route("/csresults", methods = ["POST", "GET"])
def show_cs_results():

    if request.method == "POST":
        state = request.form["state"]
        major = request.form["major"]
        loan = request.form["loan"]

    # get the state we are interested in based on state parameter
    data = db.StateWage.distinct(state)

    # store data as a dictionary
    state_wages_dict = data[0]

    coli_data = coli.find_one({"State": state})
    jm_data = job_majors.find({"Major_Category": major})
    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)
    print(job_majors_list[0]["Majors"])
    return render_template("cs-search-results.html",  coli_data=coli_data, job_majors=job_majors_list, living_wage_data=state_wages_dict)


@app.route("/hsoptions")
def collect_hs_params():
    return render_template("hs-search-params.html")


@app.route("/hsresults",  methods = ["POST", "GET"])
def show_hs_results():

    # capture parameters / user options
    if request.method == "POST":
        state = request.form["state"]
        io_state = request.form["io_state"]
        major = request.form["major"]
        timing = request.form["timing"]
    
    # track preferences for in-state vs out-of-state and timing for going to college
    pref = {}
    pref.update({"in_vs_out": io_state, "timing": timing})
    
    college_data = university.find_one({"STATE_NAME": state})

    coli_data = coli.find_one({"State": state})
    if timing == "< 1 Year":
        pref.update({"In_State_Tuition_Cost": college_data["2020-21"],
                     "Out_State_Tuition_Cost": college_data["Out_2020_2021"]})
    else:
        pref.update({"In_State_Tuition_Cost": college_data["2021-22"],
                     "Out_State_Tuition_Cost": college_data["Out_2021_2022"]})

    jm_data = job_majors.find({"Major_Category": major})

    job_majors_list = []
    for record in jm_data:
        job_majors_list.append(record)
    # print(job_majors_list[0]["Majors"])
    return render_template("hs-search-results.html",  coli_data=coli_data, job_majors=job_majors_list, college_data=college_data, pref=pref)




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
