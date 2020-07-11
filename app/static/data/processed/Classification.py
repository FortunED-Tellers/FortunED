import pandas as pd
import pymongo
import pprint as pp

def Classify(State,Major_Category,Debt):
    # Read Algo input csv
    Algo_input = pd.read_csv("static/data/processed/Algo_data_input.csv")
    
    target = Algo_input["decision"]
    target_names = ["Yes", "No"]

    data = Algo_input.drop(["decision","time_to_repay"], axis=1)
    feature_names = data.columns

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=42)

    # Support vector machine linear classifier
    from sklearn.svm import SVC 
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)

    # Model Accuracy
    # print('Test Acc: %.3f' % model.score(X_test, y_test))

    # Calculate classification report
    from sklearn.metrics import classification_report
    predictions = model.predict(X_test)
    # print(classification_report(y_test, predictions,
    #                             target_names=target_names))


    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    dbconn = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = dbconn.FortunEd

    Major_data = db.Majors.find_one({"Major_Category":Major_Category})

    Income_dict = {}
    for data in Major_data["Possible_Occupations"]:
        Occ = data["Occupation"]
        income_split =data["Median_Occ_Salary"].split(",")
        income = ''.join(map(str, income_split))
        low_25_income_split =data['Low_25_Occ_Salary'].split(",")
        low_25_pct_income = ''.join(map(str, low_25_income_split))
        recommended_ed = data['Recommended_Education']
        high_25_income_split = data['High_25_Occ_Salary'].split(",")
        high_25_pct_income =''.join(map(str, high_25_income_split))
        # pd.to_numeric(''.join(map(str, wage_split)),errors='coerce') 
        Income_dict[Occ] ={"Occ":Occ,
                          "median_income":int(pd.to_numeric(income,errors='coerce')),
                          "low_25_pct_income":int(low_25_pct_income),
                          "high_25_pct_income":int(high_25_pct_income),
                          "recommended_education":recommended_ed}

    state_wages = db.StateWage

    state_wage_list = []
    state_wage_list = list(state_wages.find())
    result_values = [i[State] for i in state_wage_list if State in i]
    result =result_values[0]
    living_wage_split = result['living wage'].split("$")[1].split(",")
    wage_join =pd.to_numeric(''.join(map(str, living_wage_split)),errors='coerce')  



    output_df = pd.DataFrame(Income_dict.values())
    output_df.columns = ["Occupation","Median_Income","Low_25_pct_income","High_25_pct_income","Recommended_Education"]
    output_df["debt"] = Debt
    output_df["living_wage"] = wage_join
    output_df["major_category"] = Major_Category

    X = output_df.loc[:,["living_wage","Median_Income","debt"]]

    predictions = model.predict(X)
  
    output_df["decision"] = predictions
    outcome = output_df.to_dict("records")
    return outcome

# pp.pprint(Classify("Alaska","Agriculture & Natural Resources",50000))
