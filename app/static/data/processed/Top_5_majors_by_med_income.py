import pymongo
import pandas as pd

def get_top_5_majors_list(Major_Category):

    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    dbconn = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = dbconn.FortunEd

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

# test = get_top_5_majors_list("Agriculture & Natural Resources")
# print(test)