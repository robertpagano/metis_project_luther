import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re 
import os
import pickle
import data_clean_functions as dcf

def find_tables(url):
    """
    This identifies html table IDs on the given URL
    """
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)


def pull_table(team, year):
    """
    This will pull a season table from baseball-reference.com when given team abbreviation and season year.
    Team abbreviations:
    'ATL', 'ARI', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET',
    'KCR', 'HOU', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK',
    'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBR', 'TEX', 'TOR', 'WSN'
    """
    url = "http://www.baseball-reference.com/teams/" + team + "/" + str(year) + "-schedule-scores.shtml"
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = "team_schedule")
    data_rows = tables[0].findAll('tr')
    data_header = tables[0].findAll('thead')
    data_header = data_header[0].findAll("tr")
    data_header = data_header[0].findAll("th")
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    header = []
    for i in range(len(data.columns)):
        header.append(data_header[i].getText())
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)


def pull_game_table(team, year):
    """
    This will pull a season table from baseball-reference.com when given team abbreviation and season year.
    Team abbreviations:
    'ATL', 'ARI', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET',
    'KCR', 'HOU', 'LAA', 'LAD', 'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK',
    'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBR', 'TEX', 'TOR', 'WSN'
    Also adding some formatting here as a test - this should give us better values for date, home vs. away
    """
    url = "http://www.baseball-reference.com/teams/" + team + "/" + str(year) + "-schedule-scores.shtml"
    dat = pull_table(team, year)
    dates = dat["Date"]
    ndates = []
    for d in dates:
        month = d.split(" ")[1]
        day = d.split(" ")[2]
        day = day.zfill(2)
        mapping = {"Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                   "Sep": "09", "Oct": "10", "Nov":"11"}
        m = mapping[month]
        ndates.append(str(year) + m + day)
    uni, counts = np.unique(ndates, return_counts = True)
    ndates = []
    for t in range(len(counts)):
        ux = uni[t]
        cx = counts[t]
        if cx == 1:
            ndates.append(ux + "0")
        else:
            for i in range(int(cx)):
                ii = i + 1
                ndates.append(ux + str(ii))
    dat["Date"] = ndates
    dat.rename(columns = {dat.columns[4] : "Location"}, inplace = True)
    homegame = []
    for g in dat["Location"]:
        homegame.append(g == "")
    dat["HomeGame"] = homegame
    dcf.rename_columns(dat)
    # dat = dcf.filter_columns(dat)
    # cols_to_keep = ['Attendance', 'Gm#', 'Date', 'Tm', 'is_home', 'Opp', 'W/L', 'runs_scored', 'runs_allowed', 'W-L', 'Rank', 'GB', 'Time', 'is_night', 'Streak']
    # return df[[cols_to_keep]]
    # dat = dat.drop(['Win', 'Loss', 'Save', 'Inn', 'Orig. Scheduled'], axis=1)
    # dat = dat[cols_to_keep]
    dcf.clean_night_game(dat)
    dcf.clean_GB_col(dat)
    dcf.clean_home_away(dat)
    dcf.split_win_loss(dat)
    dcf.calc_run_diff(dat)
    dcf.calc_win_diff(dat)
    dcf.count_cum_wins(dat)
    dcf.calc_mean_runs_last_10(dat)
    dcf.calc_run_diff(dat)
    dcf.convert_attendance(dat)
    dcf.fix_date(dat)
    return(dat)