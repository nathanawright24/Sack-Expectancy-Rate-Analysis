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
#----------------------------------------------------------------------------------------
import pandas as pd
phoebedata = pd.read_csv("C:/Users/natha/Documents/BGA/Fall 2024/SacksOverExpected/completed_df.csv")
print (phoebedata.info())
#----------------------------------------------------------------------------------------
#------------------------------ Visual Generation ---------------------------------------
#----------------------------------------------------------------------------------------
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Pocket Time Rate
sns.lmplot(
    data=phoebedata, 
    x='PktTime', 
    y='sack', 
    logistic=True, 
    scatter_kws={'alpha': 0.3}, 
    line_kws={'color': 'red'}
)
plt.gcf().set_size_inches(10, 6)
plt.title("Sack Probability vs. Pocket Time")
plt.xlabel("Pocket Time (seconds)")
plt.ylabel("Sack Probability")
plt.tight_layout()
plt.show()
#----------------------------
# Divisional Rate
sns.barplot(data=phoebedata, x='div_game', y='sack', ci=None)
plt.title("Sack Rate in Divisional vs. Non-Divisional Games")
plt.xlabel("Divisional Game (0 = No, 1 = Yes)")
plt.ylabel("Average Sack Rate")
for i, bar in enumerate(plt.gca().patches):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.00001,
        f"{height:.3f}",
        ha='center',
        va='bottom',
        fontsize=10
    )

plt.show()
#--------------------------------
# Coverage Sack Rates
phoebedata_cleanedcoverage = phoebedata.dropna(subset=['defense_coverage_type'])
print(phoebedata_cleanedcoverage['sack'].describe())

ax = sns.barplot(data=phoebedata_cleanedcoverage, x='defense_coverage_type', y='sack', ci=None, palette="muted")
plt.title("Sack Rate by Defensive Coverage Type")
plt.xlabel("Defensive Coverage Type")
plt.ylabel("Average Sack Rate")
plt.xticks(rotation=45)

for bar in ax.patches:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.00001,
        f"{height:.4f}",
        ha='center',
        va='bottom',
        fontsize=9
    )

plt.show()
"""Issue with the dataset, any plays where sacks occured has a nan
value for coverage and man/zone variables"""
#------------------------------
# PFF OL Line Graph
sns.boxplot(data=phoebedata, x='sack', y='PFFOL')
plt.title("Sack Rates by Offensive Line Grades")
plt.xlabel("Sack")
plt.ylabel("PFF Offensive Line Grade")
plt.show()
#-------------------------------
# OL Rank Graph
ol_rank_sack_rate = phoebedata.groupby('OLRank')['sack'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=ol_rank_sack_rate, x='OLRank', y='sack', marker='o', color='blue')
sns.regplot(data=ol_rank_sack_rate, x='OLRank', y='sack', scatter=False, color='red', line_kws={'linewidth': 2})
plt.title("Sack Rate by Offensive Line Rank")
plt.xlabel("Offensive Line Rank")
plt.ylabel("Average Sack Rate")
plt.xticks(range(1, 33))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#--------------------------------
# Pocket Time and Formation Interaction
pivot_table = phoebedata.pivot_table(
    index='defense_coverage_type', 
    columns='PktTime', 
    values='sack', 
    aggfunc='mean'
)
sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt=".2f")
plt.title("Pocket Time vs. Sack Rate by Defensive Formation")
plt.xlabel("Pocket Time (seconds)")
plt.ylabel("Defensive Coverage Type")
plt.show()
"""Issue with the dataset, any plays where sacks occured has a nan
value for coverage and man/zone variables"""
#-----------------------------------
# Defenders in Box Rates
defenders_in_box_sack_rate = phoebedata.groupby('defenders_in_box')['sack'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=defenders_in_box_sack_rate, x='defenders_in_box', y='sack', marker='o', color='blue')
sns.regplot(data=defenders_in_box_sack_rate, x='defenders_in_box', y='sack', scatter=False, color='red', line_kws={'linewidth': 2})
plt.title("Sack Rate by Defenders in Box")
plt.xlabel("Defenders in Box")
plt.ylabel("Average Sack Rate")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#-----------------------------------
# Man v Zone splits
"""Issue with the dataset, any plays where sacks occured has a nan
value for coverage and man/zone variables"""
#----------------------------------
# Rates on Different Surfaces
"""sns.barplot(data=phoebedata, x='', y='sack', ci=None)
plt.title("Sack Rate in Divisional vs. Non-Divisional Games")
plt.xlabel("Divisional Game (0 = No, 1 = Yes)")
plt.ylabel("Average Sack Rate")
for i, bar in enumerate(plt.gca().patches):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.00001,
        f"{height:.2f}",
        ha='center',
        va='bottom',
        fontsize=10
    )

plt.show()"""
#-----------------------------------
# Rates by Temperature
temperature_sack_rate = phoebedata.groupby('temp')['sack'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=temperature_sack_rate, x='temp', y='sack', marker='o', color='blue')
sns.regplot(data=temperature_sack_rate, x='temp', y='sack', scatter=False, color='red', line_kws={'linewidth': 2})
plt.title("Sack Rate by Temperature")
plt.xlabel("Temperature (°F)")
plt.ylabel("Average Sack Rate")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#----------------------------------
# Rates by Down and Yards to Go

#----------------------------------
# Rates by Offensive Production Rank
offense_rank_sack_rate = phoebedata.groupby('OffRank')['sack'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=offense_rank_sack_rate, x='OffRank', y='sack', marker='o', color='blue')
sns.regplot(data=offense_rank_sack_rate, x='OffRank', y='sack', scatter=False, color='red', line_kws={'linewidth': 2})
plt.title("Sack Rate by Offensive Rank")
plt.xlabel("Offensive Rank (Lower is Better)")
plt.ylabel("Average Sack Rate")
plt.xticks(range(1, 33))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#---------------------------------
# Shotgun Binary
shotgun_sack_rate = phoebedata.groupby('shotgun')['sack'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=shotgun_sack_rate, x='shotgun', y='sack', palette="muted")
for i, bar in enumerate(plt.gca().patches):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.00001,
        f"{height:.3f}",
        ha='center',
        va='bottom',
        fontsize=10)
plt.title("Sack Rate by Shotgun Formation")
plt.xlabel("Shotgun Formation (0 = No, 1 = Yes)")
plt.ylabel("Average Sack Rate")
plt.show()

#-----------------------------------
# No Huddle Binary
no_huddle_sack_rate = phoebedata.groupby('no_huddle')['sack'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=no_huddle_sack_rate, x='no_huddle', y='sack', palette="muted")
for i, bar in enumerate(plt.gca().patches):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.00001,
        f"{height:.3f}",
        ha='center',
        va='bottom',
        fontsize=10)
plt.title("Sack Rate in No Huddle")
plt.xlabel("No Huddle (0 = No, 1 = Yes")
plt.ylabel("Average Sack Rate")
plt.show()

#-----------------------------------
# xpass value