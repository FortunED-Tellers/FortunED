# import dependencies
import pandas as pd
from pprint import pprint

#function to get cost of living by City info
def Cost_of_Living_By_city():

    #url for cost of living by City
    url = 'https://www.numbeo.com/cost-of-living/region_rankings_current.jsp?region=021'

    #read_html pandas function to read table and store as a data frame
    tables = pd.read_html(url)
    COL_df_by_City = tables[2]

    #Updating rank column (returned as Nan) to value based on Index+1, data is already sorted by rank
    COL_df_by_City["Rank"] = COL_df_by_City.index +1

    #converting dataframe to dictionary format
    COL_City_dict = COL_df_by_City.to_dict("records")
    return COL_City_dict

# pprint(Cost_of_Living_By_city())

import pymongo
from pymongo import MongoClient

# connect to mongodb
client = MongoClient('mongodb://localhost:27017')

# set db connection
db = client['FortuneEd']

# set reference to collection
LivingCost_ByCity = db['LivingCost_ByCity']
LivingCost_ByCity.delete_many({})

COL_data = Cost_of_Living_By_city()
for record in COL_data:
    LivingCost_ByCity.insert_one(record)