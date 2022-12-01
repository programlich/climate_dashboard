import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq



###############################
## Global temperature change ##
###############################

# Create df for recente temperature changes
temp_recent_colnames = ["year", "human_natural", "human_natural_top", "human_natural_bottom", "natural", "natural_top", "natural_bottom", "observed" ]
temp_recent = pd.read_csv("/home/matthias/Python/Klimadashboard/Daten/gmst_changes_model_and_obs.csv", skiprows=36, skipfooter=1, names=temp_recent_colnames, header=None, engine="python")
temp_recent["dummy_data"] = 1

# linechart figure for recent temperature changes
fig_temp_line = px.line(data_frame=temp_recent, x="year", y="observed",
 labels={"year":"Jahr","observed":"Temperaturänderung / °C"},
  width=800, template="seaborn")
fig_temp_line.update_layout(xaxis_range=[1850,2023],yaxis_range=[-0.5,1.5])

# Barchart figure showing temperatur change in one selected year
fig_temp_bar = px.bar(data_frame=temp_recent,x="dummy_data",y="observed",width=400, 
            labels={"x":"Jahr","observed":"Temperaturänderung / °C","year":"Jahr"}, animation_frame="year",
            template="seaborn")
fig_temp_bar.update_xaxes(visible=False)
fig_temp_bar.update_layout(yaxis_range=[-0.5,1.5],hovermode=False)
fig_temp_bar["layout"].pop("updatemenus")

#############
# Emissions #
#############

# Import emission data per country
emissions_country = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/emissions_country.csv")

# Import emission data per capita
emissions_capita = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/emissions_country.csv")

#Import inverted and merged emissions
emissions_inverted_merged = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/emissions_inverted_merged.csv")

# Create a dict list of all countries for the dropdown menu
dict_list_countries = []
for country in emissions_inverted_merged["Country"].unique().tolist():
    this_dict = {}
    this_dict["label"] = country
    this_dict["value"] = country
    dict_list_countries.append(this_dict)
dict_list_countries

# Create dash app
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])


app.layout = dbc.Container([
            
            # Title row
            dbc.Row(
                dbc.Col(html.H1("Klimadashboard"),width={"size":6,"offset":3}),
                justify="center",style={"margin-bottom":"40px","margin-top":"20px"}),
            
            # Header row temperature graphs
            dbc.Row(
                dbc.Col(html.H2("Änderung der globalen Oberflächentemperatur relativ zum Zeitraum 1850-1900",style={"text-align":"center"}),
                width={"size":10,"offset":1},align="center"),
                justify="center"),

            # First row
            dbc.Row([
                # First col
                dbc.Col([
            
                #Temp line graph
                dcc.Graph(figure=fig_temp_line)
                        ], width=7),

                # Thermometer
                dbc.Col(children=[
                        # Uncomment the following line to switch back to plotly barchart
                        # dcc.Graph(figure=fig_temp_bar) 
                        daq.Thermometer(id="thermometer",
                                value=0.5,
                                min=-0.5,
                                max = 2,
                                showCurrentValue=True,
                                units="C",
                                color="darkred",
                                style = {"background-color":"white","color":"red",
                                        "margin-top":"5%"}),
                        html.Div(dcc.Slider(id="time_slider",value=1850,min=1850,max=2019,
                                marks={ 1850:{"label":"1850","style":{"font-size":"20px"}},
                                        1900:{"label":"1900","style":{"font-size":"20px"}},
                                        1950:{"label":"1950","style":{"font-size":"20px"}},
                                        2000:{"label":"2000","style":{"font-size":"20px"}}
                                    },
                                tooltip={"placement": "top", "always_visible": True},updatemode="drag"), #close slider

                                style={"margin-bottom":"5%"})

                                    ], # close children of thermometer col
                                width=3,style={"background-color":"white"})


                    ],align="end",justify="center",style={"margin-bottom":"30px","border":"5px solid green"}), # Close first row
       
            # Second header row
            dbc.Row(dbc.Col(html.H2("CO2 Emissionen durch Verbrennung fossiler Energieträger"),
                    width={"size":8,"offset":2}),justify="center",style={"margin-bottom":"20px"}),
            
            # Dropdown and Switch row
            dbc.Row([
                dbc.Col(
                daq.BooleanSwitch(id="cummulation_switch",
                            on=False,
                            color="blue",
                            label="Kummulierte Emissionen",
                            labelPosition="bottom"),width=3),
                dbc.Col(
                dcc.Dropdown(id="country_dd",
                        options=dict_list_countries,
                        multi=True),width=4)],
                justify="center"),

            # Emissions row  
            dbc.Row(
                dbc.Col([
                dcc.Graph(id="fig_country_capita")
                    ],width=10),justify="center",style={"margin-bottom":"20px","border":"5px solid green"}),

           
    
                ]) #close dbc container

      
@app.callback(
    Output(component_id="fig_country_capita",component_property="figure"),
    Input(component_id="country_dd",component_property="value"),
    Input(component_id="cummulation_switch",component_property="on")
)
def update_figure(selection,on):

    emissions = emissions_inverted_merged.copy(deep=True)
    
    # Show different plot if countries are selected
    if selection:

        selection_list = selection

        # Selecto only the emission data about the selected countries
        emissions = emissions.loc[emissions["Country"].isin(selection_list),:]

        if on==True:
            # Make the plot
            fig_country_capita = px.scatter(data_frame=emissions,
                                x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",color="Country", size="emissions_cumulated", 
                                labels={"emissions_country": "CO2 Emissionen pro Land / Gt ", "emissions_capita":'CO2 Emissionen pro Land pro Kopf / t ',"year":"Jahr ",
                                "emissions_cumulated":"Kummulierte Emissionen seit 1970 / Gt"}, template="seaborn",
                                hover_data={"emissions_cumulated":":.2f",
                                            "emissions_country":":.2f",
                                            "emissions_capita":":.2f"})
            fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
            fig_country_capita.update_traces(marker_size=9)
            return fig_country_capita

        elif on == False:
            # Make the plot
            fig_country_capita = px.scatter(data_frame=emissions,
                                x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",color="Country", 
                                labels={"emissions_country": "CO2 Emissionen pro Land / Gt ", "emissions_capita":'CO2 Emissionen pro Land pro Kopf / t ',"year":"Jahr "},
                                 template="seaborn",
                                hover_data={"emissions_country":":.2f",
                                            "emissions_capita":":.2f"})
            fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
            fig_country_capita.update_traces(marker_size=9)
            return fig_country_capita

    if on == True:
        # Make plot with all countries if there is no selection
        fig_country_capita = px.scatter(data_frame=emissions,
                                x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",
                                template="seaborn", size="emissions_cumulated",
                                labels={"emissions_country": "CO2 Emissionen pro Land / Gt ",
                                 "emissions_capita":'CO2 Emissionen pro Land pro Kopf / t ',"year":"Jahr "},
                                hover_data={"emissions_country":":.2f",
                                            "emissions_capita":":.2f"})
        fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
        fig_country_capita.update_traces(marker_size=8)
        
        return fig_country_capita
    
    else:
        # Make plot with all countries if there is no selection
        fig_country_capita = px.scatter(data_frame=emissions,
                                x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",template="seaborn",
                                labels={"emissions_country": "CO2 Emissionen pro Land / Gt ", "emissions_capita":'CO2 Emissionen pro Land pro Kopf / t ',"year":"Jahr "},
                                hover_data={"emissions_country":":.2f",
                                            "emissions_capita":":.2f"})
        fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
        fig_country_capita.update_traces(marker_size=8)
        
        return fig_country_capita

# Callback for the thermometer showing temperature rais in one year
@app.callback(Output(component_id="thermometer",component_property="value"),
              Input(component_id="time_slider",component_property="value"))

def update_thermometer(year):
    
    temp_recent_copy = temp_recent.copy(deep=True)
    
    if year:  
        temp = temp_recent_copy.loc[temp_recent_copy["year"]==year,"observed"].item()
        return temp
    
    

if __name__=="__main__":
    app.run_server(debug=True)
