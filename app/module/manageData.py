import pandas as pd
from pprint import pprint
import json

majors_master_path="../../data/raw/majorsMaster.csv"
majors_info_path="../../data/raw/Majors_info.csv"

occupations_wages_path= '../../data/raw/occupation_and_wage.csv'
occupations_education_path='../../data/raw/occupation and education.xlsx'

majorsMaster_df=pd.read_csv(majors_master_path)
majorsInfo_df= pd.read_csv(majors_info_path)

occupations_wages_df=pd.read_csv(occupations_wages_path)
occupations_education_df=pd.read_excel(occupations_education_path)

majorsInfo_df=majorsInfo_df.drop(columns=["Major","Major_category"])

majorsInfo_df['Major_code']=majorsInfo_df['Major_code'].astype(str)

majors_df=majorsMaster_df.merge(majorsInfo_df,left_on='FOD1P', right_on='Major_code')
majors_df=majors_df.drop(columns=["Major_code"])

mappingTable_path="../../data/raw/Majors_Ocupations_Mapping.xlsx"

mappingTable_df=pd.read_excel(mappingTable_path)

merged_df = majors_df.merge(mappingTable_df,left_on='Major_Category', right_on='Major Category',how='left')

merged_df=merged_df.dropna()

merged_df[['OcupationID','Ocupation']] = merged_df['Ocupation industry'].str.split(None, 1,expand=True) 
merged_df['OcupationID']=merged_df['OcupationID'].str.split('-',expand=True)
merged_df=merged_df.drop(columns=["Ocupation industry"])


occupations_wages_df[['occ_category_id','subid']]=occupations_wages_df['occ_code'].str.split('-',expand=True)
occupations_wages_df=occupations_wages_df.drop(columns=['area','area_title','area_type','naics','naics_title','i_group','own_code','annual','hourly','jobs_1000','loc_quotient',
                                                        'pct_total','emp_prse','mean_prse','h_mean','h_pct10','h_pct25','h_median','h_pct75','h_pct90','a_pct10','a_pct90'])

removingTitles = occupations_wages_df['subid']!='0000'
occupations_wages_df = occupations_wages_df[removingTitles]

occupations_education_df.rename(columns={'2018 National Employment Matrix title and code':'Occupation',
                                         'Unnamed: 1':'occ_code',
                                         'Typical education needed for entry':'Recomende Education'
                                        }, inplace=True)

occupations_education_df=occupations_education_df.drop(columns=['Work experience in a related occupation','Typical on-the-job training needed to attain competency in the occupation'])
occupations_education_df=occupations_education_df.dropna()

occupations_df=occupations_wages_df.merge(occupations_education_df,on='occ_code',how='left')

occupations_df=occupations_df.loc[occupations_df['o_group']=="detailed"]

def majorsFunction():
    
    MajorCategoryArray = []
    for index,row in merged_df.iterrows():
        if row.Major_Category in MajorCategoryArray:
            next
        else:
            MajorCategoryArray.append(row.Major_Category)


    mainDict={}
    for MC in MajorCategoryArray:
        majorDict={}
        for index,row in merged_df.iterrows():
            if row.Major_Category == MC:
                majorDict[row.Major]={
                    'Major_Id':row.FOD1P,
                    'Unemployment_Rate':row.Unemployment_rate,
                    'Median_Salary':row.Median,
                    'Low_25_Salary':row.P25th,
                    'High_25_Salary':row.P75th
                }
                ocupationID=row.OcupationID
                ocupationIndustry=row.Ocupation
        mainDict[MC]={'Ocupation_ID':ocupationID,
                'OcupationIndustry':ocupationIndustry,
                'Majors':majorDict}


    for key,value in mainDict.items():
        ocupationID=value['Ocupation_ID']
        possibleOcupations={}
        for index,row in occupations_df.iterrows():
            if row.occ_category_id==ocupationID:
                possibleOcupations[row.occ_title]={
                    'Occ_Code':row.occ_code,
                    'Occ_Sub_Code':row.subid,
                    'Recommended_Education':row['Recomende Education'],
                    'Median_Occ_Salary':row.a_median,
                    'Low_25_Occ_Salary':row.a_pct25,
                    'High_25_Occ_Salary':row.a_pct75
                }
        mainDict[key]['Possible_Occupations']=possibleOcupations
    
    return mainDict


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


# -- LIVING WAGE AND MEDIAN INCOME

def stateWage():
    with open('../../data/processed/state_wage_data.json') as json_file: 
        state_wage = json.load(json_file)
        

    return state_wage

def universityTuition():
    with open('../../data/processed/UniversitiesTuition.json') as json_file: 
        university_tuition = json.load(json_file)

    return university_tuition


# pprint(stateWage_data)
# print(type(stateWage_data))


# Loading MONGO
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client['FortunEd']

majors = db['Majors']
majors.delete_many({})

LivingCost = db['LivingCost']
LivingCost.delete_many({})

wageByState = db['StateWage']
wageByState.delete_many({})

tuitionUniversity = db['Universities']
tuitionUniversity.delete_many({})

majors_data=majorsFunction()
majors.update({}, majors_data, upsert=True)

COL_data = Cost_of_Living_By_State()
for record in COL_data:
    LivingCost.insert_one(record)

stateWage_data=stateWage()
wageByState.update({}, stateWage_data, upsert=True)

uniTuition_data=universityTuition()
tuitionUniversity.update({}, uniTuition_data, upsert=True)