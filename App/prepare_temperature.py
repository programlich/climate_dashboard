import pandas as pd

# Make df for temperature from 1-1990
temp_early = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/raw/SPM1_1-2000.csv")

# Make df for the temperature from 1850-2019
colnames = ["year", "human_natural", "human_natural_top", "human_natural_bottom", "natural", "natural_top", "natural_bottom", "observed" ]
temp_recent = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/raw/gmst_changes_model_and_obs.csv", skiprows=36, skipfooter=1, names=colnames, header=None, engine="python")

temp_early.to_csv("/home/matthias/Python/Klimadashboard/Analysis/data/temperature_early.csv",index=False)
temp_recent.to_csv("/home/matthias/Python/Klimadashboard/Analysis/data/temperature_recent.csv",index=False)