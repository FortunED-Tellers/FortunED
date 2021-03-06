# FortunED
### The FortunED App provides analytics for high school students, college students, and parents/guardians to project the Return on Investment (ROI) when considering majors, careers, and student loans for a college education.
<hr>

**Team:** Karl Ramsay, Swati Dontamsetti, Firzana Razak, Smiti Swain, Salvador Neves
<hr>

### Deployed Heroku Link: https://fortuned-app.herokuapp.com/

## Overview
As a team, some of us are parents, some of us are teachers, and all of us are continuing education students. We are passionate about education and the doors it can open for future career opportunities. But we understand that college can be expensive and that for some people it might not be the right route. We wanted to give a comprehensive look at the ROI of attending college for a chosen field of study. We approached this by first thinking about what each prong of our userbase would be interested in.

A high school student would be interested in:
1. The career options for a chosen field of study and the minimum degree required for each profession.
2. Specific majors under their field of study along with the salary range over time and the unemployment rate.
3. What might be the most profitable state to work in for their field of study.
4. How much tuition they might have to pay for 4 years of college.

A college student would be interested in:
1. The career options for their field of study along with entry-level salary range for each profession.
2. How long it would take to pay off their student loan.
3. What the living wage is for the state they are thinking about working in and whether there are better states to work in for their field of study.
4. What the top 5 paying majors are for their chosen field of study.

A parent/guardian would be interested in:
1. What the employment likelihood is for their child based on their gender and race in comparison to various levels of educational attainment.
2. How college tuition prices have changed for In-State and Out-of-State over time.
3. A way to access the high school or college student page to compare options for their child's future.

### Instructions
1. Open app/module folder in terminal or Git Bash.
2. Run **python manageData.py**. 
3. Open the app folder.
4. Run **python app.py**. 
5. Open browser window and type http://127.0.0.1:5000/

### Some Considerations
- All of the data is based on state universities only. It was easy to find In-State and Out-of-State tuition prices over time.
- Since we only have one University per State, we are assuming that every University offers some version of our 13 fields of study.
- Living wage is based on a single person, without any children, numbers.

![approach.png](images/FortunEd-3-Stage_Approach.png)
<br>
![detailed-approach.png](images/FortunEd-Architecture.png)

## Ingest
We used Google Sheets to split up the work of finding datasets that would allow us to present our users with thorough information. We use a lot of education, employment, and career data from the <a href="https://www.bls.gov/emp/tables.htm">US Bureau of Labor Statistics</a> (BLS). Our university tuition data comes from the <a href="https://research.collegeboard.org/trends/college-pricing">CollegeBoard</a>. Our college majors dataset comes from <a href="https://www.kaggle.com/fivethirtyeight/fivethirtyeight-college-majors-dataset/data?select=majors-list.csv">FiveThirtyEight</a>'s Kaggle dataset. Our living wage data comes from <a href="https://livingwage.mit.edu/">MIT's Living Wage Calculator</a>, which also displayed a median income per occupation that matched the BLS categories.

## Process
1. A lot of files were `Excel` or `CSV` files. We did use `Beautiful Soup` to scrape the MIT Living Wage Calculator for each state's living wage and the state's median income salary for each occupation category.
2. We used `Jupyter Notebook` to clean our datasets to just the data we are using.
3. We created mapping tables to link college majors to career categories.
4. We use `Pandas` to join the tables so that we have a link from field of study to specific majors and field of study to occupation category to specific occupations.
5. We use `Sklearn` to create two different machine learning algorithms.
  <br>a. One is a classification that determines whether a chosen state is a good place to work based on the student's loan and the state's living wage. As you can see we got two different accuracies. We used the SVM model that has a 92% accuracy.
  <br>![classification.png](images/SVM_model_CR.PNG)![classification2.png](images/Logistic_Regression_CR.PNG)
  <br>b. The other is a linear regression that extrapolated what university tuition will be for In-State and Out-of-State for the next two years.
  <br>![linear-regression.png](images/lin-regress.png)
6. We used `pymongo` and `MongoClient` to create dictionaries of all our records and then load it into `Mongo DB`.
7. We created `Python` functions to pull the specific data we need for specific charts and tables.
  <br>a. We discussed and assigned work on `Zoom` and used `Slack` to log our discussion.
  <br>![work-split.png](images/slack_group_split.png)
  <br>b. We created specific sample `HTML` pages for each group member so we could each make and test our charts/tables without overriding each other's work when pushing to `Github`.
  <br>![sample-html.jpg](images/sample_html.jpg)
8. We then met up over `Zoom` to join all our `ChartJS` scripts and `Python` functions on their corresponding `HTML`, `functions.py`, and `app.py` sections.

## Digest
The final data was stored in a `Mongo` database, which was pulled from to obtain our various datasets for the charts and tables we want to display.

We used the micro-framework `Flask` inside of `Python` to create our website that would showcase our data. We use the `Bootstrap`, `ChartJS`, and `D3JS` libraries were used to beautify our website and create dynamic visualization.

As users interface with our website the function `backend.py` tracks the selections made by a user on the front end and writes that activity to an `Excel` file. Using this logged activity, we generate a `Tableau` report to analyze user activity, engagement, and which areas we are getting the most traction. This will help in further enhancing the services and metrics collected and offered to users.

![tableau](images/tableau.png)
https://public.tableau.com/profile/smiti8274#!/vizhome/FortunED-UsageReport/FortunEDStory

## Final Website:
### Home Page
![homepage.png](images/home.png)

### High School Student Page
![highschool.png](images/hs-home.png)
![hs1.png](images/hs1.png)
![hs2.png](images/hs2.png)
![hs3.png](images/hs3.png)

### College Student Page
![college.png](images/cs-home.png)
![cs1.png](images/cs1.png)
![cs2.png](images/cs2.png)
![cs3.png](images/cs3.png)

### Parent/Guardian Page
![parents.png](images/parents-home.png)
![parents1.png](images/parents1.png)
