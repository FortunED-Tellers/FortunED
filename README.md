# FortunED
### The FortunED App provides analytics for prospective students, college students, and parents to project the Return on Investment (ROI) when considering majors, careers, and student loans for a college education.
<hr>

**Team:** Karl Ramsay, Swati Dontamsetti, Firzana Razak, Smiti Swain, Salvador Neves
<hr>

## Overview
As a team, some of use are parents, some of us are teachers, and all of us are continuing education students. We are passionate about education and the doors it can open for future career opportunities. But we understand that college can be expensive and that for some people it might not be the right route. We wanted to give a comprehensive look on the ROI of attending college for a chosen major. We approached this by first thinking about what each prong of our userbase would be interested in.

A high school student would be interested in:
1. The career options for a chosen major and the minimum degree required for each profession.
2. Specific majors under their major category along with the salary range over time and the unemployment rate.
3. What might be the most profitable state to work in for their major.
4. How much tuition they might have to pay for 4 years of college.

A college student would be interested in:
1. The career options for their major along with entry level salary range for each profession.
2. How long it would take to pay off their student loan.
3. What the living wage is for the state they are thinking about working in and whether there are better state's to work in for their major.
4. What the top 5 paying majors are for their chosen major/career category.

A parent would be interested in:
1. What the employment likelihood is for their child based on their gender and race in comparison to various levels of educational attainment.
2. How college tuition prices have changes for In-State and Out-of-State over time.
3. A way to access the high school or college student page to compare options for their child's future.

### Instructions
1. Open app/module folder in terminal or Git Bash.
2. Run **python manageData.py**. 
3. Open app folder.
4. Run **python app.py**. 
5. Open browser window and type http://127.0.0.1:5000/

### Some Considerations
- All of the data is based on state universities only. It was easy to find In-State and Out-of-State tuition prices over time.
- Since we only have one University per State, we are assuming that every University offers some version of our 13 major categories.

## The analysis was done using the ETL model.
![approach.png](app/static/img/approach.png)

## Extract
We downloaded our data from different sources. We use Census data from the <a href="https://www.labor.ny.gov/stats/nys/statewide-population-data.shtm">NY Dept of Labor</a>, the Dow Jones Index from <a href="https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI">Yahoo Finance</a>, COVID cases and deaths from <a href="https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/">USA Facts</a>, Free and Reduced-price Lunch data from <a href="https://www.nyskwic.org/get_data/indicator_data.cfm">NY State KWIC</a>, NY County Median Income by Race from the <a href="https://www.census.gov/topics/income-poverty/income/data/tables.html">Census Bureau</a>,and the GeoJSON for NY Counties from <a href="https://github.com/johan/world.geo.json/tree/master/countries/USA/NY">Github</a>.

## Transform
1. We used `VBA` to do a basic clean
2. We loaded everything into `Postgres DB` for more extensive cleaning and combining of data sources.
3. Then in `Jupyter Notebook` we used `Pandas` and the `OS` module to import our CSVs and do a final cleaning of column names, once we finalized the datasets we needed.
4. And then we performed a final merge of all the columns into one master dataset.
5. Lastly, we used `pymongo` and `MongoClient` to create dictionaries of all our records and then load it into `Mongo DB`.

## Load
The final data was stored in a `Mongo` database, which was pulled from to obtain our demographic and socio-economic results.

We used the micro-framework `Flask` inside of `Python` to create our website that would showcase our data. `Leaflet JS` and `Mapbox API` were used in `HTML` to create the map of our counties with the COVID case data used for coloring. Both the `Bootstrap`, and `ChartJS` libraries were used to beautify our website and create dynamic graphs.

![map.png](app/static/img/map.png)

![charts.png](app/static/img/charts.png)

## Final Results & Analysis
In general, our hypothesis is correct: as harder hit counties are more racially diverse and economically poor.

In the graphs presented here we'll compare Queens (the worst-hit county) with Hamilton (the least-hit county):

### Demographics
Queens is a lot **more** racially diverse compared to the state statistics.
![demoQ.png](app/static/img/demoQ.png)
Hamilton is a lot **less** racially diverse compared to the state statistics.
![demoH.png](app/static/img/demoH.png)

### Cases/Deaths & Poverty Levels
Queens had **60,236** COVID cases and is **above** the state poverty percentage.
![povQ.png](app/static/img/povQ.png)
Hamilton had **5** COVID cases and is well **below** the state poverty percentage.
![povH.png](app/static/img/povH.png)

### Median Income & Dow Jones Index
Queens is more racially diverse but the money is not spread out evenly. The white racial group tends to hold almost double the wealth of any other group, except for other (which is an ambiguous grouping with little info).
![incomeQ.png](app/static/img/incomeQ.png)
Hamilton doesn't even show data on the median income levels of the other racial groups in its county. But the white group makes about the same in Hamilton as it does in Queens, even though Queens is much poorer than Hamilton - which only makes the other racial groups in Queens that much poorer.
![incomeH.png](app/static/img/incomeH.png)
The Dow Jones Index drops in February as NY starts showing cases, it is at its lowest at end of March as we start to see the uptick in cases. But the Dow Jones Index almost immediately starts picking back up even though the COVID cases are still rising. It plateaus in April after the stimulus check is sent out on 4/9. COVID cases have seemingly (not confirmed) also platued but has not decreased yet. The stimulus may have played an effect in stabilizing the Dow Jones Index, but so too might the global control of COVID cases. There are many variables we weren't able to consider for this graph. All we know is that COVID is still on the rises, and yet the Dow Jones Index is picking up.
