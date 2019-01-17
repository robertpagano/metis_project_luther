# Project Luther

### Predicting Attendance for Struggling MLB Teams

Robert Pagano

#### Scope

In June of 2018, Rob Manfred, the commisioner of Major League Baseball, noted that attendance was down nearly 10% from the previous year. This marked the 6th season in a row of declining attendance. While the league is experimenting with rule changes to help make the game more attractive to the casual fan, I am more interested in looking into specific teams, and what could be causing their own attendance issues.

On top of this, on a team by team basis, there are a lot of businesses that could benefit from this analysis. For example, hotels in the area would have a better idea of how many bookings to expect. Bars in the area could know how to better staff. Local police could plan out resources for traffic management. The stadium itself could change their rates for advertising.

First I plan to look at the homegame data for teams that fill less than 60% of their stadiums on average on any given game in the 2018 season. This leaves us with 1134 games to analyze, with 14 different games

I will webscrape some data from baseballreference.com for some game by game data. I'll use some other sources for data such as weather, traffic, etc.



#### Methodology

1. Get all game data for 2018 for the teams chosen from baseball stats sites such as baseballreference.com and/or fangraphs.com
2. Append weather information, or any other incidental information that could come by
3. Train a linear regression model relating team and local based statistics that would predict attendence for a given game in a future season



#### Data

- Team baseball stats by game from sources such as fangraphs.com, baseballreference.com, etc.
- Weather stats / other incidental stats by zip



#### Prediction

Predicting the attendance of games by home-team 



#### Potential Features

- Win differential
- Run differential
- Number of wins last 10 games
- Mean team runs scored last 10 games (changed for whole season)
- Opp. team runs scored per game
- W-L record opposing teams
- Team salary
- Number of active allstars on roster (previous year if first half, current year if second half)
- Games out of first place
- Day of week
- Weather
- Time of first pitch
- Avg length of game
- Avg pitches per game

*NB: Note that features generally are for home team unless otherwise specified.*



#### Things to note:

There are a few other potential features I may want to explore further, and I will certainly be evolving the list as I run through models. I am also thinking of potentially picking the teams based on the variability of attendance vs. just picking those with lower attendance in general.

I may also want to take game data for 2015-2017, and see how the models for that data predict what we actually saw in 2018. As noted earlier, there has been a decline in overall attendance in that time period, so I'll need to figure out how to work with that trend.



