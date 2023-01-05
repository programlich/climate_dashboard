import pandas as pd
import locale
import os
locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

# Get path of working directory
wc_path = os.getcwd()

##########
# BUDGET #
##########

# Define a function to get the global co2 emissions of a certain year
def year_global_total_emissions(year):
    return global_total.loc[global_total["year"]==year,"total_emissions"].values[0]

# Function to calculate the remaining co2 budget per row
def calc_remaining_budget(row):

    # Get index of current row    
    this_budget_index = budget.loc[budget["date"]==row["date"]].index[0]
    
    # Get cumulated emissions until but not including the current month
    cumulated_emissions = budget.loc[0:this_budget_index-1,"emissions"].sum()
    
    remaining_budget = 400 - cumulated_emissions
    
    if remaining_budget < 0:
        remaining_budget = 0

    return remaining_budget

emissions_country = pd.read_excel(wc_path+"/App/data/raw/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx",
                                     sheet_name="fossil_CO2_totals_by_country").dropna()

# Select only global emissions an swap cols with rows
global_total = emissions_country.loc[emissions_country["Country"]=="GLOBAL TOTAL",1970:].melt(var_name="year",value_name="total_emissions")
global_total["total_emissions"] = global_total["total_emissions"]/1000 #Convert unit from Mt to Gt

# Create a df with the emissions per month and the remaining budget in this month
# The values for the years 2020 and 2021 are fetched from the emissions dataset while the 
# predicition for the upcoming months/years are calculated with the average from 2015 to 2021.

budget = pd.DataFrame()
budget["date"] = pd.date_range("2020-01-01",periods=180, freq="MS")

# Assign the measured emissions of 2020 and 2021 to these years
emissions_per_month_2020 = year_global_total_emissions(2020)/12
emissions_per_month_2021 = year_global_total_emissions(2021)/12
budget.loc[budget["date"].dt.year==2020,"emissions"] = emissions_per_month_2020
budget.loc[budget["date"].dt.year==2021,"emissions"] = emissions_per_month_2021

# Add cols for year and month
budget["year"] = budget["date"].dt.year
budget["month"] = budget["date"].dt.strftime("%B")

# Set order of columns
budget = budget[["date","year","month","emissions"]]

# Calculate average emissions from 2015 to 2021 except 2020
global_avg_15_21 = global_total.loc[global_total["year"].isin([2015,2016,2017,2018,2019,2021]),"total_emissions"].mean()
emissions_per_month_prediction = global_avg_15_21/12

# Assign the future, extrapolated emissions to all months in the df
budget.loc[~budget["date"].dt.year.isin([2020,2021]),"emissions"] = emissions_per_month_prediction

#Calculate the remaining budget
budget["remaining"] = budget.apply(calc_remaining_budget, axis=1)


budget.to_csv(wc_path+"/App/data/emissions_gauge.csv",index=False)