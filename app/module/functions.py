# The following function returns the tuition cost for a given state and time period
# This data will provide the in-state and out of state tuition metric for the given State University


def find_tution_cost(state, timing, university_data):
    college_dict = {}
    for i in range(len(university_data)):
        if university_data[i]['STATE_NAME'] == state:
            if timing == 1:
                college_dict.update({"State": state, "University": university_data[i]['University'],
                                     "InState": university_data[i]['2020-21'], "OutState": university_data[i]['Out_2020_2021']})

            elif timing == 2:
                college_dict.update({"State": state, "University": university_data[i]['University'],
                                     "InState": university_data[i]['2021-22'], "OutState": university_data[i]['Out_2021_2022']})

            else:
                college_dict.update({"State": state, "University": university_data[i]['University'],
                                     "InState": university_data[i]['2021-22'], "OutState": university_data[i]['Out_2021_2022']})

    return college_dict


# The following function will return data and labels to be used for our charts using the Chart js library.
# It take one parameter of subject - which helps to map which mongo collection and data structure we are working
# with to provide the data
def prepare_chart_data(subject, university_data):
    labels = []
    in_state_labels = []
    out_state_labels = []
    data_values = []
    in_state_values = []
    out_state_values = []

    chart_data = {}
    count_for_in_state = 0

    if subject == 'university':
        for key in university_data[0].keys():

            if not (key == '_id' or key == 'University' or key == 'STATE'):
                labels.append(key)

        labels.pop(len(labels) - 1)

        # get a count for half of the list (i.e. in-state)
        count_for_in_state = len(labels) / 2

        # break the list into two separate lists (i.e. one for in_state and one for out of state)
        for i in range(int(count_for_in_state)):
            in_state_labels.append(labels[i])

        for i in range(int(count_for_in_state)-1, (int(count_for_in_state) * 2)-1, 1):
            out_state_labels.append(labels[i])

        for value in university_data[0].values():

            if not (type(value) == str):
                data_values.append(value)

        data_values.pop(0)

        # break the list into two separate lists (i.e. one for in_state and one for out of state)
        for i in range(int(count_for_in_state)):
            in_state_values.append(data_values[i])

        for i in range(int(count_for_in_state)-1, (int(count_for_in_state) * 2)-1, 1):
            out_state_values.append(data_values[i])

        chart_data.update({'in_state_labels': in_state_labels, 'in_state_values': in_state_values,
                           'out_state_labels': out_state_labels, 'out_state_values': out_state_values})

    return chart_data

def get_state_wage(state, state_wages):
    state_wage_list = []
    state_wage_list = list(state_wages.find())
    result_values = [i[state] for i in state_wage_list if state in i]
    result =result_values[0]
    return result

def get_job_specs(db, major):
    import json

    m_j = db["majors_to_occ"]

    with open("static/data/processed/majors_to_jobs.json") as json_file:
        data_json = json.load(json_file)
        
    #Insert Data
    m_j.remove()
    m_j.insert(data_json)

    cursor = db.majors_to_occ.find({})

    jobs = []

    for document in cursor: 
        for i in document:
            if (document['major_category'] == major):
                if document['occ_title'] not in jobs:
                    jobs.append(document['occ_title'])
    
    cursor = db.majors_to_occ.find({})

    job_specs = {}

    for i in jobs:
        for document in cursor:
            if (i  == document['occ_title']):
                job_specs[i] = {'p25th':document['p25th'], 'median':document['median'], 'p75th':document['p75th']}
                break
    
    return job_specs

def four_year_cost(db, state, io_state, timing):
    university_data = db.Universities.find({})

    price = []

    for document in university_data:
        if document['STATE_NAME'] == state:
            if (timing == 1  and io_state == 'in-state'):
                price.append({'2020-21':(document['2020-21']*4), 'uni': document['University']})
            elif (timing == 2  and io_state == 'in-state'):
                price.append({'2021-22':(document['2021-22']*4), 'uni': document['University']})
            elif (timing == 1  and io_state == 'out-of-state'):
                price.append({'2020-21':(document['Out_2020_2021']*4), 'uni': document['University']})
            elif (timing == 2  and io_state == 'out-of-state'):
                price.append({'2021-22':(document['Out_2021_2022']*4), 'uni': document['University']})

    year = list(price[0].keys())[0]
    uni = price[0]['uni']
    cost = price[0][year]

    dict_ = {"year": year, "uni": uni, "cost": cost}

    return (dict_)

def bestIncomeStates(db, majorCategory):
    import pandas as pd

    state_wages = db.StateWage

    state_wage_list = list(state_wages.find())

    incomeByState={}

    for state in state_wage_list:
        for key, value in state.items():
            if key == "_id":
                next
            else:
                state= key
                listMajors=list(value.values())
                listMajors = listMajors[2:]
                majorsCatList=[]
                for MC in listMajors:
                    if MC['Major_Category'] == majorCategory:
                        salaryUnformated=MC['Average_Annual_Salary'].split("$")[1].split(",")
                        salary_list=pd.to_numeric(''.join(map(str,salaryUnformated)),errors='coerce')
                        majorsCatList.append(salary_list)

                salary=sum(majorsCatList)/len(majorsCatList)

                incomeByState[state]=salary

    incomeByState=sorted(incomeByState.items(), key=lambda x: x[1],reverse=True)

    stateAndIncome={}
    for i in range(5):
        stateAndIncome[incomeByState[i][0]]=incomeByState[i][1]

    return stateAndIncome

def whaterfall(db, state, majorCategory, debt):
    import pandas as pd

    state_wages = db.StateWage

    state_wage_list = []
    state_wage_list = list(state_wages.find())
    result_values = [i[state] for i in state_wage_list if state in i]
    result =result_values[0]
    living_wage_split = result['living wage'].split("$")[1].split(",")
    wage_state =pd.to_numeric(''.join(map(str, living_wage_split)),errors='coerce') 

    MClist=[]
    majorCatList=list(result.values())
    majorCatList = majorCatList[2:]
    for MC in majorCatList:
        if MC['Major_Category']==majorCategory:
            salaryUnformated=MC['Average_Annual_Salary'].split("$")[1].split(",")
            salary_list=pd.to_numeric(''.join(map(str,salaryUnformated)),errors='coerce')
            MClist.append(salary_list)

    salary=sum(MClist)/len(MClist)

    # salary, wage_state & debt

    paymentYear={}
    paymentYear['Year 0']={"Payed":0,
                    'Remaining':(int(debt)*(-1))}

    # time_to_repay = debt/((salary - wage_state)*0.3)
    # time_to_repay=round(time_to_repay,0)
    debtCount = (int(debt)*(-1))
    count=1
    while (debtCount<0):
        year=f'Year {count}'
        pay = (salary-wage_state)*0.3 - (debtCount*(-1)*0.06)
        debtCount=debtCount+pay
        paymentYear[year]={'Payed':round(pay,2),"Remaining":round(debtCount,2)}
        count+=1
    paymentYear[year]={'Payed':round(paymentYear[f'Year {count-2}']['Remaining']*(-1),2),"Remaining":0}
    
    return paymentYear

def get_top_5_majors_list(db, Major_Category):
    import pandas as pd
    
    Major_data = db.Majors.find_one({"Major_Category":Major_Category})

    majors_dict = {}
    for data in Major_data["Majors"]:
        major = data["Major"]
        median_salary = data["Median_Salary"]
        majors_dict[major] = pd.to_numeric(median_salary,errors='coerce') 


    majors_df = pd.DataFrame(majors_dict.items())
    majors_df.columns = ["major","median_salary"]
    majors_df.sort_values(by="median_salary", ascending=False,inplace = True)

    top_5_majors_df = majors_df.head(5)
    top_5_majors_list = top_5_majors_df['major'].values.tolist()
    
    return top_5_majors_list

def get_top_5_states_for_loan_repay(db, Major_Category,Debt):
    import pandas as pd
    from statistics import mean 

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
                               "debt":int(Debt)}
            except:
                pass
            


    output_df = pd.DataFrame(Income_dict.values())
    output_df.drop(index = 0,inplace=True)
    output_df["time_to_repay"] = output_df["debt"]/((output_df["Annual_salary"] - output_df["Living_wage"])*0.3)
    output_df.sort_values(by ="time_to_repay",inplace = True )
    top_5_states_loan_pay_off = output_df.head(5)
    top_5_states_loan_pay_off_list = top_5_states_loan_pay_off['state'].values.tolist()
   
    return top_5_states_loan_pay_off_list

def get_pay_off_period_variation(db, State,Major_Category,Debt):
    import pandas as pd
    from statistics import mean

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
        debtCount = (int(Debt)*(-1))
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
                   "Debt":int(Debt),
                   "Percentages":Percentages,
                   "time_to_repay":time_to_repay}

    return pay_off_dict