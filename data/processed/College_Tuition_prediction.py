import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression  
from pprint import pprint
import warnings
warnings.filterwarnings("ignore")



def College_Tuition_prediction():

    #Scarpe CPI data
    url = 'https://inflationdata.com/Inflation/Consumer_Price_Index/HistoricalCPI.aspx?reloaded=true'
    tables = pd.read_html(url)
    CPI_df = tables[0]
    #filter only rows above year 2007
    CPI_df = CPI_df.loc[(CPI_df["Year"] >= 2007)]
    #Calculate Average for 2020
    Average_2020 = (CPI_df.iloc[0]["Jan"] + CPI_df.iloc[0]["Feb"] + CPI_df.iloc[0]["Mar"] +CPI_df.iloc[0]["Apr"] 
                            +CPI_df.iloc[0]["May"])/5

    for i, val in CPI_df.iterrows():
        if (i ==0):
            CPI_df["Avg_CPI"] = Average_2020

    CPI_df["Ave."] = CPI_df["Ave."].fillna(CPI_df["Avg_CPI"])

    CPI_df = CPI_df[["Year","Ave."]]


    #Read Student Enrollment data
    Enrol_df =  pd.read_excel('../raw/Enrolled_Students.xlsx')  

    #Scrape Student Loan Interest Rates data
    IR_url='https://www.savingforcollege.com/article/historical-federal-student-interest-rates-and-fees'
    tables1 = pd.read_html(IR_url)
    IR_df=tables1[0]
    IR_df.drop(IR_df.index[0],inplace=True)
    IR_df=IR_df[[0,2]]
    IR_df.columns=['Year','IR']
    IR_df[['FromYear','ToYear']] = IR_df.Year.str.split("-",expand=True)
    IR_df['IR'] = IR_df['IR'].str.replace('%', '').astype(float)
    IR_df_reduced=IR_df[['FromYear','IR']]
    IR_df_reduced['FromYear']=IR_df_reduced['FromYear'].astype(int)


    #Merge Data Frames based on inner joins
    Combined_Enroll_CPI = pd.merge(Enrol_df,CPI_df,how="inner")
    Combined_Enroll_CPI_IR = pd.merge(Combined_Enroll_CPI,IR_df_reduced,how="inner",left_on='Year', right_on='FromYear')

    # X inputs to model from 2007 to 2018
    Enroll_X_Inputs = Combined_Enroll_CPI_IR.loc[(Combined_Enroll_CPI_IR["Year"] <= 2018)]
    X = Enroll_X_Inputs[["Ave.","Total","IR"]]

    # New X inputs for 2019 and 2020 to be used in Model predictions for 2020 and 2021
    X_new_inputs = Combined_Enroll_CPI_IR.tail(2)
    X_new_inputs_reduced = X_new_inputs[["Ave.","Total","IR"]]

    #Read In State College Tuition
    Tuition_df =  pd.read_excel('../processed/college_Tuition_in_State.xlsx')  

    #Prediction for In-State Tuition Fees
    university = {}

    # loop through all universities
    for i in Tuition_df.index:
        Univ = Tuition_df['University'][i]
        # print(Tuition_df['University'][i])
        University = Tuition_df.iloc[[i]]
        University_T = University.transpose()
        University_T = University_T[i]
        y_values = University_T.values

        #prepare y values one year ahead of X year(i.e from 2008-2019)
        y = []
        for i in y_values:
            try:
                i_int = int(i)
                y.append(i_int)
            except:
                pass
        y.pop(0)
        
        #Model, Fit, Predict
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        training_score = model.score(X_train, y_train)
        testing_score = model.score(X_test, y_test)
        # print(f"Model Training Score: {training_score}")
        # print(f"Model Testing Score: {testing_score}")
        
        prediction_2020 = model.predict([X_new_inputs_reduced.iloc[0]])
        prediction_2021 = model.predict([X_new_inputs_reduced.iloc[1]])
        
        # print(f"Actual In-State Tuition 2019-2020: {y[11]}")
        # print(f"Pedicated In-State Tuition 2020-2021: {prediction_2020}")
        # print(f"Pedicated In-State Tuition 2021-2022: {prediction_2021}")
        # print("----------------------------------------")
        university[Univ] = {"2020-21": prediction_2020[0],
                        "2021-22":prediction_2021[0]}    

    # In State Tuition Prediction to Data Frame
    Predicted_df = pd.DataFrame.from_dict(university)
    Predicted_df = Predicted_df.transpose()

    # Prediction merged with intial data frame
    In_State_Tuition_df = pd.merge(Tuition_df,Predicted_df,how = "inner",left_on="University", right_on=Predicted_df.index)



    # read out of state Tuition data
    Out_State_Tuition_df = pd.read_excel('../processed/college_Tuition_out_of_State.xlsx')  

    #Prediction for Out-of-State Tuition Fees
    out_university = {}
    for i in Out_State_Tuition_df.index:
        Univ = Tuition_df['University'][i]
        # print(Out_State_Tuition_df['University'][i])
        University = Out_State_Tuition_df.iloc[[i]]
        University_T = University.transpose()
        University_T = University_T[i]
        y_values = University_T.values

        #prepare y values one year ahead of X year(i.e from 2008-2019)
        y = []
        for i in y_values:
            try:
                i_int = int(i)
                y.append(i_int)
            except:
                pass
        y.pop(0)
        
        #Model, Fit, Predict
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        training_score = model.score(X_train, y_train)
        testing_score = model.score(X_test, y_test)
        # print(f"Model Training Score: {training_score}")
        # print(f"Model Testing Score: {testing_score}")
        
        prediction_2020 = model.predict([X_new_inputs_reduced.iloc[0]])
        prediction_2021 = model.predict([X_new_inputs_reduced.iloc[1]])
        
        # print(f"Actual Out-of-State Tuition 2019-2020: {y[11]}")
        # print(f"Pedicated Out-of-State Tuition 2020-2021: {prediction_2020}")
        # print(f"Pedicated Out-of-State Tuition 2021-2022: {prediction_2021}")
        # print("----------------------------------------")
        out_university[Univ] = {"2020-21": prediction_2020[0],
                        "2021-22":prediction_2021[0]}    

    # Out of State Prediction data to DataFrame
    Out_State_Predicted_df = pd.DataFrame.from_dict(out_university)
    Out_State_Predicted_df = Out_State_Predicted_df.transpose()

    # Predictions merged with intial dataframe
    Out_Tuition_df = pd.merge(Out_State_Tuition_df,Out_State_Predicted_df,how = "inner",left_on="University", right_on=Predicted_df.index)
    Out_Tuition_df.columns = ["University","Out_2007_08","Out_2008_09","Out_2009_10","Out_2010_11","Out_2011_12","Out_2012_13",
                            "Out_2013_14","Out_2014_2015","Out_2015_2016","Out_2016_2017","Out_2017_2018","Out_2018_2019","Out_2019_2020",
                            "Out_2020_2021","Out_2021_2022"]

    # Merged In-State and Out of State dataframes
    In_Out_Tuition_df = pd.merge(In_State_Tuition_df,Out_Tuition_df,how="inner",on="University")

    # State and intials dictionary to dataframe
    states = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut",
          "DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana",
          "IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
          "MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada",
          "NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota",
          "OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
          "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington",
          "WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}

    stateInitial = pd.DataFrame(list(states.items()),columns = ['STATE','STATE_NAME']) 

    # final Tuition DataFrame with merged State name 
    Final_Tuition_df = pd.merge(In_Out_Tuition_df,stateInitial,how = "inner")

    #Final Tuition Dictionary by State
    Tuition_dict = {}
    for i in Final_Tuition_df.index:
        State = Final_Tuition_df['STATE'][i]
        STATE_NAME = Final_Tuition_df['STATE_NAME'][i]
        Univ = Final_Tuition_df['University'][i]
        
        In_Cost_2007 = Final_Tuition_df['2007-08'][i]
        In_Cost_2008 = Final_Tuition_df['2008-09'][i]
        In_Cost_2009 = Final_Tuition_df['2009-10'][i]
        In_Cost_2010 = Final_Tuition_df['2010-11'][i]
        In_Cost_2011 = Final_Tuition_df['2011-12'][i]
        In_Cost_2012 = Final_Tuition_df['2012-13'][i]
        In_Cost_2013 = Final_Tuition_df['2013-14'][i]
        In_Cost_2014 = Final_Tuition_df['2014-15'][i]
        In_Cost_2015 = Final_Tuition_df['2015-16'][i]
        In_Cost_2016 = Final_Tuition_df['2016-17'][i]
        In_Cost_2017 = Final_Tuition_df['2017-18'][i]
        In_Cost_2018 = Final_Tuition_df['2018-19'][i]
        In_Cost_2019 = Final_Tuition_df['2019-20'][i]
        In_Cost_2020 = round(Final_Tuition_df['2020-21'][i])
        In_Cost_2021 = round(Final_Tuition_df['2021-22'][i])
        
        Out_Cost_2007 = Final_Tuition_df["Out_2007_08"][i]
        Out_Cost_2008 = Final_Tuition_df['Out_2008_09'][i]
        Out_Cost_2009 = Final_Tuition_df['Out_2009_10'][i]
        Out_Cost_2010 = Final_Tuition_df['Out_2010_11'][i]
        Out_Cost_2011 = Final_Tuition_df['Out_2011_12'][i]
        Out_Cost_2012 = Final_Tuition_df['Out_2012_13'][i]
        Out_Cost_2013 = Final_Tuition_df['Out_2013_14'][i]
        Out_Cost_2014 = Final_Tuition_df['Out_2014_2015'][i]
        Out_Cost_2015 = Final_Tuition_df['Out_2015_2016'][i]
        Out_Cost_2016 = Final_Tuition_df['Out_2016_2017'][i]
        Out_Cost_2017 = Final_Tuition_df['Out_2017_2018'][i]
        Out_Cost_2018 = Final_Tuition_df['Out_2018_2019'][i]
        Out_Cost_2019 = Final_Tuition_df['Out_2019_2020'][i]
        Out_Cost_2020 = round(Final_Tuition_df['Out_2020_2021'][i])
        Out_Cost_2021 = round(Final_Tuition_df['Out_2021_2022'][i])
            
                    
        Tuition_dict[State] = {"State_ID" : State,
                            "State_name" : STATE_NAME,
                            "University":Univ,
                            "In_State_Tuition_2007-2008":In_Cost_2007,
                            "In_State_Tuition_2008-2009":In_Cost_2008,
                            "In_State_Tuition_2009-2010":In_Cost_2009,
                            "In_State_Tuition_2010-2011":In_Cost_2010,
                            "In_State_Tuition_2011-2012":In_Cost_2011,
                            "In_State_Tuition_2012-2013":In_Cost_2012,
                            "In_State_Tuition_2013-2014":In_Cost_2013,
                            "In_State_Tuition_2014-2015":In_Cost_2014,
                            "In_State_Tuition_2015-2016":In_Cost_2015,
                            "In_State_Tuition_2016-2017":In_Cost_2016,
                            "In_State_Tuition_2017-2018":In_Cost_2017,
                            "In_State_Tuition_2018-2019":In_Cost_2018,
                            "In_State_Tuition_2019-2020":In_Cost_2019,
                            "In_State_Tuition_2020-2021":In_Cost_2020,
                            "In_State_Tuition_2021-2022":In_Cost_2021,
                            "Out_of_State_Tuition_2007-2008":Out_Cost_2007,
                            "Out_of_State_Tuition_2008-2009":Out_Cost_2008,
                            "Out_of_State_Tuition_2009-2010":Out_Cost_2009,
                            "Out_of_State_Tuition_2010-2011":Out_Cost_2010,
                            "Out_of_State_Tuition_2011-2012":Out_Cost_2011,
                            "Out_of_State_Tuition_2012-2013":Out_Cost_2012,
                            "Out_of_State_Tuition_2013-2014":Out_Cost_2013,
                            "Out_of_State_Tuition_2014-2015":Out_Cost_2014,
                            "Out_of_State_Tuition_2015-2016":Out_Cost_2015,
                            "Out_of_State_Tuition_2016-2017":Out_Cost_2016,
                            "Out_of_State_Tuition_2017-2018":Out_Cost_2017,
                            "Out_of_State_Tuition_2018-2019":Out_Cost_2018,
                            "Out_of_State_Tuition_2019-2020":Out_Cost_2019,
                            "Out_of_State_Tuition_2020-2021":Out_Cost_2020,
                            "Out_of_State_Tuition_2021-2022":Out_Cost_2021}    

    return Tuition_dict

# pprint(College_Tuition_prediction())

# import pymongo
# from pymongo import MongoClient

# # connect to mongodb
# client = MongoClient('mongodb://localhost:27017')

# # set db connection
# db = client['FortunED']

# # set reference to collection
# Universities = db['Universities']
# Universities.delete_many({})   

# Universities_data = College_Tuition_prediction()
# # Universities.update_many({},Universities_data,upsert=True)

# for record in Universities_data:
#     Universities.insert_one(record)





