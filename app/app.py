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
db = dbconn.FortunEd

majors = db.Majors

# Define routes
# @app.route("/")
# def welcome():
#     return render_template('index.html')


@app.route("/")
def results():
    majors_data = majors.find_one()
    return render_template('results.html', master_major_data=majors_data)


# @app.route("/hs.html")
# def highschool():
#     return render_template('hs.html')


# @app.route("/college.html")
# def college():
#     return render_template('college.html')


# @app.route("/guardian.html")
# def guardian():
#     return render_template('guardian.html')


# # @app.route("/results.html/<state>, <in_out>,<major>,<timeframe>")
# # def HS_Visualization(major):
# #     cost_data = db.cost_analysis.find_one({"major": f"{major}", "state"})
# #     income_data = db.income_analysis.find_one({"major": f"{major}"})
# #     options_data = db.options_analysis.find_one({"major": f"{major}"})
# #     outlook_data = db.outlook_analysis.find_one({"major": f"{major}"})
# #     predict_data = db.outlook_analysis.find_one({"major": f"{major}"})

#     master_major_data = []

#     if cost_data is not None:
#         master_major_data.append(cost_data["education_cost"])

#     if income_data is not None:
#         master_major_data.append(Income_data["avg_income"])

#     if options_data is not None:
#         master_major_data.append(options_data["job_options"])

#     if outlook_data is not None:
#         master_major_data.append(outlook_data["no_of_jobs"])

#     if predicted_data is not None:
#         master_major_data.append(predict_data["other_population"])

#     print(master_major_data)

#     return render_template('results.html', master_major_data=master_major_data)
#     else:
#         return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
