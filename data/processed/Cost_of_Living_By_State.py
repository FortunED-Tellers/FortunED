# import dependencies
import pandas as pd
from pprint import pprint

#function to get cost of living by State info
def Cost_of_Living_By_State():

    #url for cost of living by State
    url = 'https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state'

    #read_html pandas function to read table and store as a data frame
    tables = pd.read_html(url)
    COL_df_by_State = tables[0]

    #converting dataframe to dictionary format
    COL_State_dict = COL_df_by_State.to_dict("records")
    return COL_State_dict

pprint(Cost_of_Living_By_State())