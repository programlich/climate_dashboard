import pandas as pd

# Make df for temperature from 1-1990
temp_early = pd.read_csv("../../data/raw/SPM1_1-2000.csv")

# Make df for the temperature from 1850-2019
col_names = ["year", "human_natural", "human_natural_top", "human_natural_bottom", "natural", "natural_top",
             "natural_bottom", "observed"]
temp_recent = pd.read_csv("../../data/raw/gmst_changes_model_and_obs.csv", skiprows=36, skipfooter=1, names=col_names,
                          header=None, engine="python")

temp_early.to_csv("../../data/clean/temperature_early.csv", index=False)
temp_recent.to_csv("../../data/clean/temperature_recent.csv", index=False)
