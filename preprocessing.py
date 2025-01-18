# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:55:15 2024

@author: NAWri
"""

import nfl_data_py as nfl
import pandas as pd

stats_21 = pd.read_csv("C:/Users/NAWri/Documents/BGA/4th_Down_Prob/2021Stats.csv")
stats_22 = pd.read_csv("C:/Users/NAWri/Documents/BGA/4th_Down_Prob/2022Stats.csv")
stats_23 = pd.read_csv("C:/Users/NAWri/Documents/BGA/4th_Down_Prob/2023Stats.csv")

columns = ['Year','Team','OffRank','PFFOL','OLRank']
blocking_21 = stats_21[columns]
blocking_22 = stats_22[columns]
blocking_23 = stats_23[columns]

seasons = [2021,2022,2023]
pbp_data = nfl.import_pbp_data(seasons)
passes = pbp_data[pbp_data['play_type']=='pass']

stats_21 = stats_21.rename(columns={
    'Year':'season'})
stats_22 = stats_22.rename(columns={
    'Year':'season'})
stats_23 = stats_23.rename(columns={
    'Year':'season'})

combined_stats = pd.concat([stats_21, stats_22, stats_23], ignore_index=True)

#Changing LA to LA Rams (LAR)
import re

# Iterate over each column in the dataframe
for column in passes.columns:
    # Check if the column contains strings (dtype == 'object')
    if passes[column].dtype == 'object':
        # Replace "LA" with "LAR" using regular expressions with word boundaries
        passes[column] = passes[column].apply(lambda x: re.sub(r'\bLA\b', 'LAR', x))
        
combined_stats = combined_stats.rename(columns={
    'Team':'posteam'})   

passplays = pd.merge(
    combined_stats,
    passes,
    left_on=['posteam', 'season'],
    right_on=['posteam', 'season'],
    how='left'
)
def save_passplays_to_csv():
    filepath = "C:/Users/NAWri/Documents/BGA/passplays.csv"
    passplays.to_csv(filepath, index=False)
save_passplays_to_csv()

import pandas as pd
passplays = pd.read_csv("C:/Users/NAWri/Documents/BGA/sacksoverexpected/passplays.csv")

columnstokeep = ['posteam','season','OLRank','OffRank','PFFOL','down','ydstogo',
                 'was_pressure','yardline_100','shotgun','no_huddle','qb_scramble',
                 'score_differential','wp','vegas_wp','qb_hit','sack','passer_player_id',
                 'passer_player_name','qb_hit_1_player_id','qb_hit_1_player_name',
                 'qb_hit_2_player_id','qb_hit_2_player_name','sack_player_id','sack_player_name',
                 'half_sack_1_player_id','half_sack_1_player_name','half_sack_2_player_id',
                 'half_sack_2_player_name','surface','temp','xpass','pass_oe','offense_formation',
                 'offense_personnel','defenders_in_box','number_of_pass_rushers','defense_players',
                 'was_pressure','defense_man_zone_type','defense_coverage_type','div_game',
                 'td_prob','fg_prob']   

passplaysfiltered = passplays[columnstokeep]

def save_passplaysfiltered_to_csv():
    filepath = "C:/Users/NAWri/Documents/BGA/sacksoverexpected/passplaysfiltered.csv"
    passplaysfiltered.to_csv(filepath, index=False)
save_passplaysfiltered_to_csv()
