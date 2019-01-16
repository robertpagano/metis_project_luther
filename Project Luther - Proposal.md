# Project Luther

### Predicting Attendance for Struggling MLB Teams





In June of 2018, Rob Manfred, the commisioner of Major League Baseball, noted that attendance was down nearly 10% from the previous year. This marked the 6th season in a row of declining attendance. While the league is experimenting with rule changes to help make the game more attractive to the casual fan, I am more interested in looking into specific teams, and what could be causing their own attendance issues.

On top of this, on a team by team basis, there are a lot of businesses that could benefit from this analysis. For example, hotels in the area would have a better idea of how many bookings to expect. Bars in the area could know how to better staff. Local police could plan out resources for traffic management. The stadium itself could change their rates for advertising.

We would ignore teams who sellout more than 60% of their games (this number could change based on analysis)

Thinking of using mostly baseball game statistics

First I plan to look at the homegame data for teams that fill less than 60% of their stadiums on average on any given game in the 2018 season. This leaves us with 1134 games to analyze, with 14 different games

I will webscrape some data from baseballreference.com for some game by game data. I'll use some other sources for data such as weather



#### Methodology

1. Get all game data for 2018 for the teams chosen from baseball stats sites such as baseballreference.com and/or fangraphs.com
2. Append weather information, or any other incidental information that could come by
3. Train a linear regression model relating team and local based statistics that would predict attendence for a given game in a future season



#### Data

