def get_pay_off_period_variation(State,Major_Category,Debt):
    import pymongo
    import pandas as pd
    import pprint as pp
    from statistics import mean


    # State = "Alaska"
    # Major_Category = "Agriculture & Natural Resources"
    # Debt = 50000

    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    dbconn = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = dbconn.FortunEd


    state_wages = db.StateWage

    state_wage_list = list(state_wages.find())
    state_values = [i[State] for i in state_wage_list if State in i]
    state_dict = state_values[0]
    living_wage_split = state_dict['living wage'].split("$")[1].split(",")
    living_wage =pd.to_numeric(''.join(map(str, living_wage_split)),errors='coerce') 

    majors_list = [i for i in state_dict.values() if 'Major_Category' in i]
    salary_list = []
    for  MC in majors_list:
        if MC['Major_Category']==Major_Category:
            salaryUnformated=MC['Average_Annual_Salary'].split("$")[1].split(",")
            salary=pd.to_numeric(''.join(map(str,salaryUnformated)),errors='coerce')
            salary_list.append(salary)
    annual_salary = mean(salary_list)
    Percentages = [20, 30, 50]
    time_to_repay = []
    for percent in Percentages:
        debtCount = Debt*(-1)
        count=1
        paymentYear = {}
        while (debtCount<0):
                year=f'Year {count}'
                pay = (annual_salary-living_wage)*percent/100 - (debtCount*(-1)*0.06)
                debtCount=debtCount+pay
                paymentYear[year]={'Payed':round(pay,2),"Remaining":round(debtCount,2)}
                count+=1
        paymentYear[year]={'Payed':round(paymentYear[f'Year {count-2}']['Remaining']*(-1),2),"Remaining":0}
        time_to_repay.append(len(paymentYear))
    pay_off_dict = {"state":State,
                   "living_wage":living_wage,
                   "major_category":Major_Category,
                   "annual_salary":annual_salary,
                   "Debt":Debt,
                   "Percentages":Percentages,
                   "time_to_repay":time_to_repay}

    return pay_off_dict

# print(get_pay_off_period_variation("Alaska","Agriculture & Natural Resources",50000))