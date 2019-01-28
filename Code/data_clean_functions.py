import numpy as np
import pandas as pd


def rename_columns(df):
	"""
	this will clean up some of the names already existing from bbref
	"""
	df = df.rename(columns={'R': 'runs_scored', 'RA': 'runs_allowed', 'HomeGame': 'is_home', 'D/N': "is_night"}, inplace = True)
	return df


def filter_columns(df):
	"""
	this will filter out the unneeded columns. Not sure why but need to drop columns and then re-order, so that's what I am doing
	"""
	cols_to_keep = ['Attendance', 'Gm#', 'Date', 'Tm', 'is_home', 'Opp', 'W/L', 'runs_scored', 'runs_allowed', 'W-L', 'Rank', 'GB', 'Time', 'is_night', 'Streak']
	# return df[[cols_to_keep]]
	df.drop(['Win', 'Loss', 'Save', 'Inn', 'Orig. Scheduled'], axis=1, inplace = True)
	df = df[cols_to_keep]
	return df


def clean_night_game(df):
	df['is_night'].replace('N','1',inplace=True)
	df['is_night'].replace('D','0',inplace=True)
	df['is_night'] = pd.to_numeric(df['is_night'])


def clean_GB_col(df):
	"""
	this will clean up 'games back' column so it can be used numerically
	"""
	df['GB'] = df['GB'].str.replace('Tied', '0')
	df['GB'] = df['GB'].str.replace('up ', '-')
	df['GB'] = df['GB'].str.replace('down ', '')
	df['GB'] = df['GB'].str.replace('up', '-')
	df['GB'] = df['GB'].str.replace('down', '')
	df['GB'] = pd.to_numeric(df['GB'])
	return df


def clean_home_away(df):
	"""
	this will clean up the home/away column so 'home' will be 1 and 'away' will be 0
	"""
	df['is_home'] = df['is_home'].astype(int)
	return df


def split_win_loss(df):
	"""
	this will split wins or losses into their own columns
	"""
	win_loss = df['W-L'].str.split('-', expand=True)
	df['Total_wins'] = win_loss[0]
	df['Total_losses'] = win_loss[1]
	df[['Total_wins', 'Total_losses']] = df[['Total_wins', 'Total_losses']].apply(pd.to_numeric)
	return df


def calc_win_diff(df):
	df['Win_differential'] = df['Total_wins'] - df['Total_losses']
	return df


def count_cum_wins(df):
	"""
	this first converts wins to a '1', and then counts the cumulative wins in last 10 games
	"""
	df['win_value'] = df['W/L'].str.replace("W", "1")
	df['win_value'] = df['win_value'].str.replace("L", "0")
	df['win_value'] = df['win_value'].str.replace("0-wo", "0")
	df['win_value'] = df['win_value'].str.replace("1-wo", "1")
	df['win_value'] = df['win_value'].str.replace("1 &X", "1")
	df['win_value'] = df['win_value'].str.replace("0 &X", "0")
	df['win_value'] = df['win_value'].str.replace("1 &V", "1")
	df['win_value'] = df['win_value'].str.replace("0 &V", "0")
	df['win_value'] = df['win_value'].str.replace("1 &H", "1")
	df['win_value'] = df['win_value'].str.replace("0 &H", "0")
	df['win_value'] = df['win_value'].str.replace("1 &Y", "1")
	df['win_value'] = df['win_value'].str.replace("0 &Y", "0")
	df['win_value'] = df['win_value'].str.replace("1 &P", "1")
	df['win_value'] = df['win_value'].str.replace("0 &P", "0")
	df['win_value'] = df['win_value'].str.replace("T", "0")
	df['win_value'] = pd.to_numeric(df['win_value'])
	df['Wins_last_10'] = df['win_value'].rolling(min_periods=10, window=10).sum()
	return df

def calc_mean_runs_last_10(df):
	"""
	calculates the mean runs per last 10 games
	"""
	df['Mean_runs_last_10'] = df['runs_scored'].rolling(min_periods=1, window=10).mean()
	return df

def calc_run_diff(df):
	"""
	calculates the running run differential per game
	"""
	df[['runs_scored', 'runs_allowed']] = df[['runs_scored', 'runs_allowed']].apply(pd.to_numeric)
	df['cum_runs_scored'] = df['runs_scored'].cumsum()
	df['cum_runs_allowed'] = df['runs_allowed'].cumsum()
	df['run_differential'] = df['cum_runs_scored'] - df['cum_runs_allowed']
	return df

def convert_attendance(df):
	"""
	turns attendance value into a numerical
	"""
	df['Attendance'] = df['Attendance'].str.replace(',','')
	df['Attendance'] = pd.to_numeric(df['Attendance'])
	return df

def fix_date(df):
	"""
	sets a year, month, and day column. Will still need to figure out how to add this as a regression variable
	"""
	df['date_fixed'] = df['Date'].astype(int).floordiv(10)
	df['year'] = df.Date.str[0:4]
	df['month'] = df.Date.str[4:6]
	df['day'] = df.Date.str[6:8]
	return df

# def filter_reg_columns(df):
# 	"""
# 	grabs just the columns needed for regression - to update later
# 	"""
# 	df_reg_test = df[['Attendance', 'Gm#', 'Rank', 'GB', 'is_night', 'is_home', 'Win_differential', 'Wins_last_10', 'Mean_runs_last_10', 'run_differential']]
# 	return df



def clean_team(df):
	rename_columns(df)
	# df = filter_columns(df)
	clean_night_game(df)
	clean_GB_col(df)
	clean_home_away(df)
	split_win_loss(df)
	calc_win_diff(df)
	calc_run_diff(df)
	count_cum_wins(df)
	calc_mean_runs_last_10(df)
	calc_run_diff(df)
	convert_attendance(df)
	fix_date(df)
	# df = filter_reg_columns(df)

	return df



