import pandas as pd

# Function for calculating the cumulated emissions of a country
def calc_cumulated_emissions(row):
    year = row["year"]
    country = row["Country"]

    cumulated_emissions = emissions_inverted_merged.loc[(emissions_inverted_merged["year"]<=year) & (emissions_inverted_merged["Country"]==country),"emissions_country"].sum()
    
    return cumulated_emissions

# Import emission per country data
emissions_country = pd.read_excel("/home/matthias/Python/Klimadashboard/Analysis/data/raw/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", 
                                    sheet_name="fossil_CO2_totals_by_country").dropna()

# Import emission per capita data
emissions_capita = pd.read_excel("/home/matthias/Python/Klimadashboard/Analysis/data/raw/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx",
                                 sheet_name="fossil_CO2_per_capita_by_countr",skipfooter=3).dropna()


# Create inverted df for country emissions
emissions_country_inverted = emissions_country.drop(emissions_country.tail(1).index).drop("Substance",axis=1).melt(id_vars=["Country","EDGAR Country Code"],var_name="year",value_name="emissions")

# Create inverted df for per capita emissions
emissions_capita_inverted = emissions_capita.drop(emissions_capita.tail(1).index).drop("Substance",axis=1).melt(id_vars=["EDGAR Country Code","Country"], var_name="year",value_name="emissions")

# Merge the two dfs
emissions_inverted_merged = pd.merge(left=emissions_country_inverted, right=emissions_capita_inverted, on=["EDGAR Country Code","Country","year"],suffixes=["_country","_capita"])

# Convert country emissions from Mt to Gt
emissions_inverted_merged["emissions_country"] = emissions_inverted_merged["emissions_country"] / 1000

emissions_inverted_merged["emissions_cumulated"] = emissions_inverted_merged.apply(calc_cumulated_emissions, axis=1)

emissions_inverted_merged.to_csv("/home/matthias/Python/Klimadashboard/Analysis/data/emissions_inverted_merged.csv",index=False)