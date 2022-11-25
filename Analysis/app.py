import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

###############################
## Global temperature change ##
###############################

# Create df for recente temperature changes
temp_recent_colnames = ["year", "human_natural", "human_natural_top", "human_natural_bottom", "natural", "natural_top", "natural_bottom", "observed" ]
temp_recent = pd.read_csv("/home/matthias/Python/Klimadashboard/Daten/gmst_changes_model_and_obs.csv", skiprows=36, skipfooter=1, names=temp_recent_colnames, header=None, engine="python")
temp_recent["dummy_data"] = 1

# Create linechart figure for recent temperature changes
fig_temp_line = px.line(data_frame=temp_recent, x="year", y="observed",
 labels={"year":"Jahr","observed":"Temperaturänderung / °C"},
  #title="Jährliche Änderung der globalen Oberflächentemperatur relativ zum Zeitraum 1850-1900",
  width=800)
fig_temp_line.update_layout(xaxis_range=[1850,2023],yaxis_range=[-0.5,1.5])

""" # Create barchart figure plotting the temperatur change in one certain year
year = 2019
fig_temp_bar = px.bar(data_frame=temp_recent, x=temp_recent.loc[temp_recent["year"]==year,
            "year"],y=temp_recent.loc[temp_recent["year"]==year,"observed"],width=400,
            labels={"x":"Jahr","y":"Temperaturänderung / °C"})
fig_temp_bar.update_xaxes(visible=False)
fig_temp_bar.update_layout(yaxis_range=[0,1.6]) """

fig_temp_bar = px.bar(data_frame=temp_recent,x="dummy_data",y="observed",width=400,
            labels={"x":"Jahr","observed":"Temperaturänderung / °C","year":"Jahr"}, animation_frame="year" )
fig_temp_bar.update_xaxes(visible=False)
fig_temp_bar.update_layout(yaxis_range=[-0.5,1.5],hovermode=False)
fig_temp_bar["layout"].pop("updatemenus")

# Import emission data per country
emissions_country = pd.read_excel("/home/matthias/Python/Klimadashboard/Daten/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx",
                                 sheet_name="fossil_CO2_totals_by_country").dropna()
# Import emission data per capita
emissions_capita = pd.read_excel("/home/matthias/Python/Klimadashboard/Daten/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx",
                                 sheet_name="fossil_CO2_per_capita_by_countr",skipfooter=3).dropna()

# Create inverted df for country emissions
emissions_country_inverted = emissions_country.drop(emissions_country.tail(1).index).drop("Substance",axis=1).melt(id_vars=["Country","EDGAR Country Code"],var_name="year",value_name="emissions")
# Create inverted df for per capita emissions
emissions_capita_inverted = emissions_capita.drop(emissions_capita.tail(1).index).drop("Substance",axis=1).melt(id_vars=["EDGAR Country Code","Country"], var_name="year",value_name="emissions")
# Merge the two dfs
emissions_inverted_merged = pd.merge(left=emissions_country_inverted, right=emissions_capita_inverted, on=["EDGAR Country Code","Country","year"],suffixes=["_country","_capita"])
# Convert country emissions from Mt to Gt
emissions_inverted_merged["emissions_country"] = emissions_inverted_merged["emissions_country"] / 1000

dict_list_countries = []
for country in emissions_inverted_merged["Country"].unique().tolist():
    this_dict = {}
    this_dict["label"] = country
    this_dict["value"] = country
    dict_list_countries.append(this_dict)
dict_list_countries


app = dash.Dash()

app.layout = html.Div(children=[
    
    # Header
    html.H1("Klimadashboard",
        style={'display':'block', "text-align":"center"}),
    
        #First row
        html.Div([
            # Subheader
            html.H2("Änderung der globalen Oberflächentemperatur relativ zum Zeitraum 1850-1900",
                style={"text-align":"center"}),
            
            #Temp line graph
            html.Div(dcc.Graph(figure=fig_temp_line),
                style={"display":"inline-block","margin":"10px auto",
                        "width":"70%"}),
            
            # Bar temp graph    
            html.Div(dcc.Graph(figure=fig_temp_bar), style={"display":"inline-block", "width":"30%", "margin":"10px auto"})],
            # Styling first row
                style={'width':'90%','margin':"10px auto", 
                            "border":"2px solid green"}
                ), #Close first row
        

        # Second row
        html.Div([
            
            # Header second row
            html.H2("CO2 Emissionen durch Verbrennung fossiler Energieträger",style={"text-align":"center"}),
            # Country dropdown
            html.Div(
            dcc.Dropdown(id="country_dd",
                options=dict_list_countries,
                        multi=True),   

                    style={"width":"20%","margin":"10px auto", 
                            "display":"block"}  
                    ),   

            # Emissions country/capita plot
            html.Div(dcc.Graph(id="fig_country_capita"),
                style={"width":"90%","margin":"10px auto",
                        "display":"block"})


                ], #closing second row children

            # Styling second row
            style={'width':'90%','margin':"10px auto", 
                            "border":"2px solid green"}

                )

        ])  # Close global div
                           
      
@app.callback(
    Output(component_id="fig_country_capita",component_property="figure"),
    Input(component_id="country_dd",component_property="value")
)
def update_figure(selection):

    emissions = emissions_inverted_merged.copy(deep=True)
    
    if selection:
        if type(selection) == str:
            selection_list = []
            selection_list.append(selection)
        selection_list = selection
        
        emissions = emissions.loc[emissions["Country"].isin(selection_list),:]
    
        fig_country_capita = px.scatter(data_frame=emissions,
                             x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",color="Country",
                            labels={"emissions_country": "CO2 Emissionen pro Land / Gt ", "emissions_capita":'CO2 Emissionen pro Land pro Kopf / t ',"year":"Jahr "})
        fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
        fig_country_capita.update_traces(marker_size=9)
        return fig_country_capita
    
    fig_country_capita = px.scatter(data_frame=emissions,
                             x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",
                            labels={"emissions_country": "CO2 Emissionen pro Land / Gt ", "emissions_capita":'CO2 Emissionen pro Land pro Kopf / t ',"year":"Jahr "})
    fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
    fig_country_capita.update_traces(marker_size=8)
    
    return fig_country_capita


if __name__=="__main__":
    app.run_server(debug=True)
