# Forecasting MLB Game Attendance

### **Project Luther** 

##### Robert Pagano - January 27th, 2019



## Summary



Of all the major sports in North America, the MLB has the most number of games per year. Each team in the league will host 81 home games every season, and each game has major implications for not only the baseball organization itself, but local businesses and public services in the area as well.

Regarding the team itself, this information could be very useful for:

- pricing tickets
- adjust marketing
- selling advertising
- planning promotions

For businesses in the area, it would be helpful to know when it will be more or less crowded. Hotels, for example, could use this information to target their advertising to out-of-town fans if they expect a sellout crowd.

And finally, public services in the area, such as the Police, could use this information to more effectively allocate resources.

My objectives for this project were to figure out as much as I could about attendance through:

- collecting data for every MLB regular season game from 2014-2018. This data includes our target, attendance, as well as mostly baseball stats, such as how many hits were in any given game, how many runs did each team score, and what day each game was played on
- Manipulate the data to be able to measure how well a team was doing throughout the year and have this updated on a game by game basis
- Use linear regression modelling to predict attendance level given a set of features from the data

I will break out the above in more detail below, where I will explain how I acquired the data, what types of features I then created, and how I made decisions around modeling.



## Tools and Packages Used



- Pandas
- NumPy
- Matplotlib
- seaborn
- scikit-learn
- BeautifulSoup
- Jupyter Notebook
- Sublime Text



## Data Collection and Feature Selection

I used BaseballReference for the large majority of my final data. I used BeautifulSoup to scrape all of the game-by-game season data for every team from 2014-2018. Each team and year combination is one page, so I wrote a script that would take in a team name and year, and return a Pandas dataframe representing that team's season. Each of these 150 dataframes (30 teams * 5 seasons) were merged together to create 24300 rows of data. After filtering for home games only, and removing a small number of rows without attendance data, the final data had 12318 rows, each representing one game in the 5 year period.

My approach for determining what data I should be using was to focus on two general area - what data indicated that a team was more or less exciting (how many games have they been winning, how many runs have they been scoring, etc.), and what data indiciated that a specific game was going to be more or less popular than another game outside of the home game's success (what day of the week it is, who is the opposing team, etc.).

The original data set only included statistics that came from each specific game, but in order to get the full story of how a team was doing at that specific time in their season, I knew I was going to need to calculate cumulative features. 

Below is a list of all of the features - 11 were used in the final model:

| Feature                | Used in final model | Description                                                  | Note                                |
| ---------------------- | ------------------- | ------------------------------------------------------------ | ----------------------------------- |
| Attendance             | Target variable     | Attendence of each game                                      |                                     |
| Gm#                    |                     | Running total of number of games played in given season      |                                     |
| Tm                     |                     | Home team                                                    |                                     |
| Opp                    |                     | Away Team                                                    |                                     |
| Rank                   | X                   | Where the team is placed in their division - 1 is in first, 5 is last |                                     |
| GB                     | X                   | Games back from the division lead. Teams in first are <=0    |                                     |
| is_night               | X                   | Day or night game                                            | categorical                         |
| run_differential       | X                   | Calculated by keeping a running total of runs scored vs. runs allowed | Custom feature created              |
| Win_differential       | X                   | Calculated by keeping a running total of wins vs. losses     | Custom feature created              |
| Wins_last_10           | X                   | Represents numner of wins in team's last 10 games            | Custom feature created              |
| Mean_runs_last_10      |                     | Running total of the mean amount of runs the team is averaging over last 10 games | Custom feature created              |
| batter_age             | X                   | Average age of batters on the home team                      |                                     |
| current_all_stars      | X                   | Number of players on home team that were in the All-Star game in previous year |                                     |
| lifetime_all_stars     | X                   | Number of players on home team that were in the All-Star ever |                                     |
| player_salary          | X                   | Total team salary for given year                             |                                     |
| Opp_Wins_last_10       |                     | Away team version of the above                               | Custom feature created              |
| Opp_Win_differential   |                     | Away team version of the above                               | Custom feature created              |
| Opp_Rank               |                     | Away team version of the above                               | Custom feature created              |
| Opp_GB                 |                     | Away team version of the above                               | Custom feature created              |
| Opp_Mean_runs_last_10  |                     | Away team version of the above                               | Custom feature created              |
| opp_batter_age         |                     | Away team version of the above                               | Custom feature created              |
| opp_current_all_stars  |                     | Away team version of the above                               | Custom feature created              |
| opp_lifetime_all_stars |                     | Away team version of the above                               | Custom feature created              |
| opp_player_salary      |                     | Away team version of the above                               | Custom feature created              |
| is_weekend             | X                   | If 1, day is Friday, Saturday, or Sunday                     | Custom feature created, categorical |
| stadium_cap            |                     | Maximum capacity of stadium                                  |                                     |



As you can see from the above, I created opponent features that pull in the statistical data and salary/all-star information from the opposing team. To my surprise, each of these had very low correlations with attendance, so I decided to keep them out. I do think there is a way to capture interest in the away team and how it is associated with attendance, but that is for future work. Below are the aforementioned correlations:

![image-20190127182040218](/Users/robertpagano/Library/Application Support/typora-user-images/image-20190127182040218.png)



## Model Analysis and Results



I set up a workflow for my model analysis that tested several different models using cross validation on 5 folds for 80% of the data, leaving 20% of the data aside as our test.

After several iterations, I selected 11 features (from above), and cross validated them using RidgeCV and LassoCV to determine the best lambda value for each, and to see if I was holding on to any features that would "zero" out from this process. In the end, I was happy with selecting a Lasso model with standardized features. When this model was tested on my test data, it achived a RMSE of 7124, and an R^2 of 0.434. 

![img](https://lh3.googleusercontent.com/08Hf5zlmE798nN-qfm6h3tEMXV1kZByRT17MrDU7-TFHH5NNw6ofy1pBNdFHImnMWVrOFRQOMjQ8tTJE9K-0zzqk4ycnzXQjxz-vSRzPI2u-v-D5YaCOn6cxAEpgKwUkpreP5coVVtg)





## Future Work



There are many more angles to look into this data should there be more time. Just as some examples, one could:

- Transform the Y variable. If you review the image of the residuals above, you can see that they tend to get smaller on the positive side of the line towards the end. I believe this is due to sellout games, and how if they are predicted, the error can only be on the negative end of the spectrum. My initial idea is to take a ratio of each attendance from it's maximum attendance, and subtract that value from one to get a % of empty seats in each game. Taking a log value of this woukld hypothetically make the results more normally distributed, which could then help with the strength of the model
- Add additional years to the data easily using the scraping and cleaning scripts
- See how the model predicts specific teams, or groups of teams (such as specific divisions / leagues, teams with lower attendance, etc.) and compare the results to each other. I believe this could provide some additional valuable insight, as maybe some features are much more important to specific types of teams than others
- The features that ended up having the highest coefficients were somewhat surprising to me - team combined salary and the amount of 'lifetime' all-stars that were on the team. The fact that these two features did not highly correlate with actual winning teams seems to suggest that "star power" has a lot more to do with attendance than actually getting wins 
- I also assumed that there would be more features for opposing teams that would highly correlate with attendance values, but the ones I chose seemed to not have much of an effect. I think this could be an avenue to explore more deeply, because there are certainly at least several teams in the league that always draw in big crowds when they visit other ballparks
- Adding weather data could also significantly improve the model, however, could also weaken the true predictive power as it's not always so easy to know how the weather will be in advance



## What I would do differently



- One lesson I learned while working with my dataset and with the data scraping process was just how important the order of things mattered. A lot of the features that I created were combinations and cumulative statistics that really only made sense when in the context of a specific team in a specific season. So I learned that I needed to actually create my data cleaning and manipulation functions, and then import them to my web scraping script, so they could be done for each team/season combination, before all of the data was then combined together. In retrospect, this seems somewhat obvious, but it was definitely an a-ha moment when I discovered the reason behind my counts not making sense.



