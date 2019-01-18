import numpy as np
import pandas as pd


def rename_columns(df):
	"""
	this will clean up some of the names already existing from bbref
	"""
	df = df.rename(columns={'Unnamed: 4': 'home_or_away', 'R': 'runs_scored', 'RA': 'runs_allowed'}, inplace = True)
	return df


def filter_columns(df):
	"""
	this will filter out the unneeded columns. Not sure why but need to drop columns and then re-order, so that's what I am doing
	"""
	cols_to_keep = ['Attendance', 'Gm#', 'Date', 'Tm', 'home_or_away', 'Opp', 'W/L', 'runs_scored', 'runs_allowed', 'W-L', 'Rank', 'GB', 'Time', 'D/N', 'Streak']
	# return df[[cols_to_keep]]
	# df.drop(['Unnamed: 2', 'Win', 'Loss', 'Save', 'Inn', 'Orig. Scheduled'], axis=1, inplace = True)
	df = df[cols_to_keep]
	return df


def clean_GB_col(df):
	"""
	this will clean up 'games back' column so it can be used numerically
	"""
	df['GB'] = df['GB'].str.replace('Tied', '0')
	df['GB'] = df['GB'].str.replace('up ', '')
	df['GB'] = df['GB'].str.replace('down ', '')
	df['GB'] = pd.to_numeric(df['GB'])
	return df


def clean_home_away(df):
	"""
	this will clean up the home/away column so 'home' can be filtered on
	"""
	df['home_or_away'].fillna(value='Home', inplace=True)
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


def calc_win_differential(df):
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
	df['cum_runs_scored'] = df['runs_scored'].cumsum()
	df['cum_runs_allowed'] = df['runs_allowed'].cumsum()
	df['run_differential'] = df['cum_runs_scored'] - df['cum_runs_allowed']
	return df

# def reorder_cols(df):
# 	df = df['Attendance', 'Gm#', 'Date', 'Tm', 'home_or_away', 'Opp', 'W/L', 'runs_scored', 'runs_allowed', 'W-L', 'Rank', 'GB', 'Time', 'D/N', 'Streak', 'Total_wins', 'Total_losses', 'Win_differential', 'win_value', 'Wins_last_10', 'Mean_runs_last_10', 'cum_runs_scored', 'cum_runs_allowed', 'run_differential']
# 	return df

def clean_team(df):
	df = rename_columns(df)
	df = filter_columns(df)
	# df = clean_GB_col(df)
	# df = clean_home_away(df)
	# df = split_win_loss(df)
	# df = calc_run_diff(df)
	# df = count_cum_wins(df)
	# df = calc_mean_runs_last_10(df)
	# df = calc_run_diff(df)
	return df





