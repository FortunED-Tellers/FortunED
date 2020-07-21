import pandas as pd
from pprint import pprint
import pymongo
import json

# -- COST OF LIVING

def Cost_of_Living_By_State():

    #url for cost of living by State
    url = 'https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state'

    #read_html pandas function to read table and store as a data frame
    tables = pd.read_html(url)
    COL_df_by_State = tables[0]

    #converting dataframe to dictionary format
    COL_State_dict = COL_df_by_State.to_dict("records")
    return COL_State_dict




def universityTuition():
    with open('../static/data/processed/UniversitiesTuition.json') as json_file: 
        university_tuition = json.load(json_file)

    return university_tuition


# pprint(stateWage_data)
# print(type(stateWage_data))


# Loading MONGO
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

#client = pymongo.MongoClient("mongodb+srv://fort_user:TCU7sGNl3Y3OyEnM@cluster0.wv5gd.mongodb.net/fortuned?retryWrites=true&w=majority")
db = client.fortuned




db = client['FortunEd']

majors = db['Majors']
majors.delete_many({})

def majorsInfo():
    with open('../static/data/processed/Majors.json') as json_file: 
        majors_info = json.load(json_file)
        majors_info_list= majors_info['MajorCategories']

        for MC in majors_info_list:
            majors.insert(MC)
    return majors_info

majorsInfo()

LivingCost = db['LivingCost']
LivingCost.delete_many({})

wageByState = db['StateWage']
wageByState.delete_many({})

# -- LIVING WAGE AND MEDIAN INCOME

def stateWage():
    with open('../static/data/processed/state_wage_data_redo.json') as json_file: 
        state_wage = json.load(json_file)
        state_wage_list = state_wage["data"]
        
        for records in state_wage_list:
            wageByState.insert(records)
        

    return state_wage

stateWage()

m_j = db["majors_to_occ"]

with open("../static/data/processed/majors_to_jobs.json") as json_file:
    data_json = json.load(json_file)
        
#Insert Data
m_j.remove()
m_j.insert(data_json)


tuitionUniversity = db['Universities']
tuitionUniversity.delete_many({})



COL_data = Cost_of_Living_By_State()
for record in COL_data:
    LivingCost.insert_one(record)

# stateWage_data=stateWage()
# wageByState.update({}, stateWage_data, upsert=True)

uniTuition_data=universityTuition()
# tuitionUniversity.update({}, uniTuition_data, upsert=True)
for record in uniTuition_data:
    tuitionUniversity.insert_one(record)