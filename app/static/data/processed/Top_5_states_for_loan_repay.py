def get_top_5_states_for_loan_repay(Major_Category,Debt):
    import pymongo
    import pandas as pd
    import pprint as pp
    from statistics import mean 

    # Major_Category = "Business"
    # Debt = 50000


    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    dbconn = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = dbconn.FortunEd

    Income_dict = {}

    state_wages = db.StateWage

    state_wage_list = list(state_wages.find())
    for record in state_wage_list:

        for key,value in record.items():
            State = key
            try:
                living_wage_split = value['living wage'].split("$")[1].split(",")
                living_wage =pd.to_numeric(''.join(map(str, living_wage_split)),errors='coerce')

                result_values = [i for i in value.values() if 'Major_Category' in i]
                salary_list = []
                for  MC in result_values:
                    if MC['Major_Category']==Major_Category:
                        salaryUnformated=MC['Average_Annual_Salary'].split("$")[1].split(",")
                        salary=pd.to_numeric(''.join(map(str,salaryUnformated)),errors='coerce')
                        salary_list.append(salary)
                annual_salary = mean(salary_list)
                Income_dict[key] = {"state":State,
                               "Major_category":Major_Category,
                               "Living_wage":living_wage,
                               "Annual_salary":annual_salary,
                               "debt":Debt}
            except:
                pass
            


    output_df = pd.DataFrame(Income_dict.values())
    output_df.drop(index = 0,inplace=True)
    output_df["time_to_repay"] = output_df["debt"]/((output_df["Annual_salary"] - output_df["Living_wage"])*0.3)
    output_df.sort_values(by ="time_to_repay",inplace = True )
    top_5_states_loan_pay_off = output_df.head(5)
    top_5_states_loan_pay_off_list = top_5_states_loan_pay_off['state'].values.tolist()
    return top_5_states_loan_pay_off_list

# print(get_top_5_states_for_loan_repay("Business",80000))