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

pprint(Cost_of_Living_By_city())