import pandas as pd
import pprint as pp
import json

def majorsFunction():

    majors_master_path="../raw/majorsMaster.csv"
    majors_info_path="../raw/Majors_info.csv"

    occupations_wages_path= '../raw/occupation_and_wage.csv'
    occupations_education_path='../raw/occupation and education.xlsx'

    majorsMaster_df=pd.read_csv(majors_master_path)
    majorsInfo_df= pd.read_csv(majors_info_path)

    occupations_wages_df=pd.read_csv(occupations_wages_path)
    occupations_education_df=pd.read_excel(occupations_education_path)

    majorsInfo_df=majorsInfo_df.drop(columns=["Major","Major_category"])

    majorsInfo_df['Major_code']=majorsInfo_df['Major_code'].astype(str)

    majors_df=majorsMaster_df.merge(majorsInfo_df,left_on='FOD1P', right_on='Major_code')
    majors_df=majors_df.drop(columns=["Major_code"])

    mappingTable_path="../raw/Majors_Ocupations_Mapping.xlsx"

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

    MajorCategoryArray = []
    for index,row in merged_df.iterrows():
        if row.Major_Category in MajorCategoryArray:
            next
        else:
            MajorCategoryArray.append(row.Major_Category)

    mainList=[]
    for MC in MajorCategoryArray:
        mainDict={}
        majorList=[]
        for index,row in merged_df.iterrows():
            majorDict={}
            if row.Major_Category == MC:
                majorDict["Major"]=row.Major
                majorDict["Major_Id"]=row.FOD1P
                majorDict["Unemployment_Rate"]=row.Unemployment_rate
                majorDict["Median_Salary"]=row.Median
                majorDict["Low_25_Salary"]=row.P25th
                majorDict["High_25_Salary"]=row.P75th

                ocupationID=row.OcupationID
                ocupationIndustry=row.Ocupation
                majorList.append(majorDict)
        mainDict["Major_Category"]=MC
        mainDict["Ocupation_ID"]=ocupationID
        mainDict["OcupationIndustry"]=ocupationIndustry
        mainDict["Majors"]=majorList
        mainList.append(mainDict)

    # pp.pprint(mainList)


    for MajCat in mainList:
        ocupationID=MajCat['Ocupation_ID']
        occlist=[]
        for index,row in occupations_df.iterrows():
            possibleOcupations={}
            if row.occ_category_id==ocupationID:
                possibleOcupations['Occupation']=row.occ_title
                possibleOcupations['Occ_Code']=row.occ_code
                possibleOcupations['Occ_Sub_Code']=row.subid
                possibleOcupations['Recommended_Education']=row['Recomende Education']
                possibleOcupations['Median_Occ_Salary']=row.a_median
                possibleOcupations['Low_25_Occ_Salary']=row.a_pct25
                possibleOcupations['High_25_Occ_Salary']=row.a_pct75
                occlist.append(possibleOcupations)
        
        MajCat['Possible_Occupations']=occlist

    majorsOccupations_dict={}
    majorsOccupations_dict["MajorCategories"]=mainList

    # pp.pprint(majorsOccupations_dict)

    return majorsOccupations_dict

majors_data = majorsFunction()

with open('majors.json', 'w') as f:
    json.dump(majors_data, f)