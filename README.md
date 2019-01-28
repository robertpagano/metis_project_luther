# Forecasting MLB Game Attendance
Metis Project 2: Project Luther - Web Scraping and Linear Regression



### Data sources

- game by game stats, including attendance: https://www.baseball-reference.com/teams/TBR/2018-schedule-scores.shtml
- weather data (not yet added as a feature, but is scraped): https://mesonet.agron.iastate.edu/request/download.phtml



### Goal

- Attempting to predict game attendance for a given MLB team using game-by-game statistics and other features derived from each specific team



### Tools

- Pandas

- NumPy

- Matplotlib

- seaborn

- scikit-learn

- BeautifulSoup

- Jupyter Notebook

- Sublime Text

  

### How to use

- Coming soon - files are organized but will do a writeup for specific order to get from selecting your data to scrape, to having cleaned features ready for modeling. You can more or less follow along with my process in the "Code, data, and notebooks" section for the time being



### Code, data, and notebooks

#### Code files

- /code/bbref_scrape.py - this is used to select the team and year to be scraped
- /code/data_clean_functions - these functions are imported into bbref_scrape, as the data is cleaned each time the web scraper is used

#### Jupyter Notebooks

- Final Regressions.ipnyb - here is my final modelling file. This includes plots of my residual analysis, and a few other EDA type plots
- Merged MLB game data - 2014-2018 V3 FINAL.ipnyb - here is where I prepared my data files for my model file.
- bbref scraper-FINAL.ipnyb - this is where I tested and completed my scraping of baseball reference 
- EDA work.ipnyb - EDA file

#### Data files

*Here I will be listing the data files that were used in chronological order. Please note that some of the paths may need to be edited as I upded the folder organization:*

- merged_data_2014_2018_final_uncleaned.pickle - this contains the final scraped data from baseball reference, that was then imported to be cleaned
- merged_data_initial_clean_V2.pickle - the cleaned version of the above
- merged_df_added_opp_values_FINAL.pickle - same as above, but merged data from away team in each row. Not used in modelling yet
- regression_data_v3_max_features.pickle - cleaned data but filtered for specific features (22 features)
- regression_data_v3_less_features.pickle - Same as above but filtered for just 12 features. This is what was used in final analysis
- regression_data_v3_att_cap_less_features.pickle - same as above, but with a log transformed version of the target variable (not used)



### Summary files

- **Forecasting MLB Game Attendance.pdf** - Presentation Slides
- **Forecasting MLB Game Attendance - Writeup ** - High level written summary of project
- **Project Luther - Proposal** - Original proposal for project idea