# FortunED
The FortunED App provides analytics for professionals, students and parents to project the Return on Investment (ROI) when considering student loans and other funding for college education.
# NYCares
### A deep dive analysis into the impact COVID-19 has had on different counties within New York.
<hr>

**Team:** Karl Ramsay (Project Manager - Back-End), Swati Dontamsetti (Front-End), Firzana Razak (Front-End), Amber Martin (Back-End), Oswaldo Moreno (Back-End), Anthony Brown (Back-End)
<hr>

## Overview
With a potential plateau in COVID-19 cases in NY, but no definite decrease as of yet, we are interested into seeing what the impact has been on the different counties of NY. We look into the demographic and socio-economic breakdown of each county, while keeping in mind how the impact has varied from county to county.

*Hypothesis: Harder hit counties are poorer and more racially diverse.*

We also wanted to see what the correlation is between Wall St and Main St. We know that the stock market crashed pretty severely but is picking back up again, which is disconnected from the way every day people are dealing with COVID-19 since cases have yet to decrease.

*Hypothesis: The stimulus has a stabilizing effect on the market, even though cases are still rising.*

### Instructions
1. Open app/module folder in terminal or Git Bash.
2. Run **python load_mongo_db.py**. 
3. Open app folder.
4. Run **python app.py**. 
5. Open browser window and type http://127.0.0.1:5000/

### Some Considerations
- All of the data was collected on May 22nd, and was analyzed for that date.
- All the demographic and socio-economic data is from the Census, which is a self-reported entity. So the numbers for racial groups may not be completely accurate.
- Hispanic/Latino on the Census is more of an ethnicity than a racial group. There can be white-hispanics, black-hispanics, etc. We used the non-hispanic data for all the racial groups except for other, and subtracted the total county population from all those data points to get the hispanic data point (so it may be skewed).
- Other is an ambiguous grouping that includes two-or-more races, so a half-white, or half-asian, etc. is not broken down nor included in the other groups. This also skews graph for the median income, since family/inhereted wealth is a big part of the incomes people end up reaching. In short, the other racial group does not provide a detailed picture, and can alter the perception of the results in some counties.

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
