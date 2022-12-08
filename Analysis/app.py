import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq
import datetime as dt
import plotly.graph_objects as go
import os
from dash_bootstrap_templates import load_figure_template
import locale

from components import ssp_checklist, ssp_modal

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
dbc_css = os.path.abspath("assets/dbc.min.css")
template = "superhero"

load_figure_template(template)


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
  width=800, template=template)
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

# Yearly global co2 emissions
global_total = emissions_country.loc[emissions_country["Country"]=="GLOBAL TOTAL",
                                    "1970":].melt(var_name="year",value_name="total_emissions")
global_total["year"] = global_total["year"].astype(int)

# Calculate the average global co2 emissions between 2015 and 2021. Year 2020 will not be part of the average because the emissions 
# where quite low due to the covid pandemic                                 
global_avg_15_21 = global_total.loc[global_total["year"].isin([2015,2016,2017,2018,2019,2021]),"total_emissions"].mean()

def year_global_total_emissions(year):
    return global_total.loc[global_total["year"]==year,"total_emissions"].item()

# Emissions of 2020 and 2021
emissions_20_21 = (year_global_total_emissions(2020) + year_global_total_emissions(2021))

# Emissions since january 2022
average_global_co2_per_second = global_avg_15_21/365/24/60/60 * 1000000000  #value in t/s
time_since_jan22 = dt.datetime.now() - dt.datetime(2022,1,1)  #Time difference between jan 2020 and now
used_since_jan_22 = time_since_jan22.total_seconds() * average_global_co2_per_second  /1000000000 #Used co2 budget since jan2020 in Gt

# Remaining co2 budget
remaining_budget = 400 - emissions_20_21/1000 - used_since_jan_22/1000    #Remaining co2 budget in Gt


##########
# Budget
##########
budget = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/emissions_gauge.csv")

#####################
# CO2 concentration #
#####################
concentration = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/co2_concentration_total.csv")


############
# DASH APP #
############

# Create dash app
app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO,dbc_css])


app.layout = dbc.Container([
            
            # Title row
            dbc.Row(
                dbc.Col(html.H1("Klimadashboard"),width={"size":6,"offset":3}),
                justify="center",style={"margin-bottom":"40px","margin-top":"20px"}),
            

            # concentration and budget row
            dbc.Row([
                dbc.Col([
                    html.H2("CO2 Konzentration in der Atmosphäre",style={"textAlign":"center"}),
                    dcc.Graph(id="fig_concentration")
                ], width=6), #close fig col

                dbc.Col([
                    html.Br(),
                    html.Br(),
                     ssp_checklist, #Select certain ssp data
                     ssp_modal      #Explenation on ssp 
                     
                ], width=1),
                dbc.Col([
                        html.H2("CO2 Budget / Gt",style={"textAlign":"center"}),
                        html.Br(),
                        html.Div([
                                daq.Gauge(id ="fig_emissions_gauge",
                                    showCurrentValue=True,
                                    value=200,
                                    max=400,
                                    min=0,
                                    color = "darkred"
                                    )],style={"textAlign":"center","margin-top":"4px"}),
                        html.H3(id="month_budget",style={"textAlign":"center"}),

                   
                        html.Div(dcc.Slider(id="gauge_slider",min=1,max=180,
                                marks={ 1:{"label":"2020","style":{"font-size":"20px"}},
                                        60:{"label":"2025","style":{"font-size":"20px"}},
                                        120:{"label":"2030","style":{"font-size":"20px"}},
                                        180:{"label":"2035","style":{"font-size":"20px"}}
                                    },
                                        updatemode="drag"), #close slider

                                style={"margin-bottom":"5%"}), #close slider Div
                            
                        html.Div(
                            dbc.Button("Heute",outline=True,color="danger",id="button_today",n_clicks=0),
                            style={"textAlign":"center","margin-bottom":"5%",}
                        )
         
                        ],width=4)

            ],style={"margin-bottom":"20px"}), #close concentration row

            # Second header row
            dbc.Row(dbc.Col(html.H2("CO2 Emissionen durch Verbrennung fossiler Energieträger"),
                    width={"size":8,"offset":2}),justify="center",style={"margin-bottom":"20px"}),
            
            # Dropdown and Switch row
            dbc.Row([
                dbc.Col(
                dbc.Switch(id="cummulation_switch",
                            value=False,
                            
                            label="Kummulierte Emissionen",
                            #labelPosition="bottom"
                            ),width=3),
                dbc.Col(
                dcc.Dropdown(id="country_dd",
                        options=dict_list_countries,
                        multi=True),width=4)],
                justify="center",style={"margin-bottom":"10px"}),

            # Emissions row  
            dbc.Row(
                dbc.Col([
                dcc.Graph(id="fig_country_capita")
                    ],width=10),justify="center",style={"margin-bottom":"20px"}),


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
                                style = {"background-color":"white",
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
                                width=3)


                    ],align="end",justify="center",style={"margin-bottom":"30px"}), # Close first row
       

           
          

            
                ],className="dbc") #close dbc container

# Callback for CO2 concentration
@app.callback(Output(component_id="fig_concentration",component_property="figure"),
              Input(component_id="ssp_checklist",component_property="value")
)

def checklist(checked):
    concentration_copy = concentration.copy(deep=True)
    
    show_list = ["gemessen"] + checked  #Select all lines to be shown

    # Select all the corresponding colors to the selected data
    color_dict = {"value":["gemessen","ssp119",'ssp126','ssp245','ssp370','ssp585'],
            "color":["red","blue","green","yellow","grey","darkred"]}
    color_df = pd.DataFrame(color_dict)
    color_list = []
    for line in show_list:
        color_list.append(color_df.loc[color_df["value"]==line,"color"].item())
    
    # Create line chart 
    fig = px.line(data_frame=concentration_copy,x="year",y=show_list, color_discrete_sequence=color_list,
                 labels={"value":"CO2 Konzentration / ppm","year":"Jahr","variable":""})
    fig.update_traces(hovertemplate=None)
    
    if "ssp370" in checked or "ssp585" in checked:
        fig.update_layout(hovermode="x",yaxis_range=[250,1200])
    else:
        fig.update_layout(hovermode="x",yaxis_range=[250,650])

    return fig

# Callback for the modal giving information about the ssps
@app.callback(
    Output(component_id="ssp_modal", component_property="is_open"),
    [Input(component_id="open_ssp_modal", component_property="n_clicks"),
    Input(component_id="close_ssp_modal", component_property="n_clicks")],
    State(component_id="ssp_modal",component_property="is_open")
)

def toggle_modal(click_open, click_close, is_open):
    if click_open or click_close:
        return not is_open
    return is_open



# Callback for gauge
@app.callback(Output(component_id="fig_emissions_gauge", component_property="value"),  # gauge figure
              Output(component_id="month_budget",component_property="children"),        # selected month and year
              Output(component_id="button_today",component_property="n_clicks"),        # click output -> set to 0
              Output(component_id="gauge_slider",component_property="value"),           # position on slider
              Input(component_id="gauge_slider",component_property="value"),            # slider input
              Input(component_id="button_today",component_property="n_clicks"))         # click input 

def update_gauge(slider,today_click):

    budget_copy = budget.copy(deep=True)    #create copy of the data
    budget_copy.index += 1  #Increas index by one to make slider work correctly
    # Get todays month and year
    today_year = dt.datetime.now().year
    today_month = dt.datetime.now().strftime("%B")

    # Case 0: Initial state
    this_budget = budget_copy.loc[(budget_copy["year"]==today_year) & (budget_copy["month"]==today_month),"remaining"].item()
    date = f"{today_month} {today_year}"
    slider_value = budget_copy.loc[(budget_copy["year"]==today_year) & (budget_copy["month"]==today_month),"remaining"].index[0]
    
    # Case 1: Slider moved
    if slider:
        this_budget = budget_copy.loc[slider, "remaining"]
        this_month = budget_copy.loc[slider,"month"]
        this_year = budget_copy.loc[slider,"year"]
        date = f"{this_month} {this_year}"
        slider_value = slider
    
    # Case 2: Button clicked
    if today_click:
        this_budget = budget_copy.loc[(budget_copy["year"]==today_year) & (budget_copy["month"]==today_month),"remaining"].item()
        date = f"{today_month} {today_year}"
        slider_value = budget_copy.loc[(budget_copy["year"]==today_year) & (budget_copy["month"]==today_month),"remaining"].index[0]
    
    gauge = daq.Gauge(
        showCurrentValue=True,
        units="Gt",
        value=this_budget,
        max=400,
        min=0
        )
    n_clicks = None
    return this_budget,date,n_clicks,slider_value

    # Create the gauge
    gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = this_budget,
    domain = {'x': [0, 1], 'y': [0, 1]},
    
    gauge = {'axis': {'range': [None, 400]},
            'borderwidth': 4,
            'bordercolor': "darkgray",
            'steps' : [
                {'range': [0, 200], 'color': "#ebebeb"},
                {'range': [200, 400], 'color': "#ebebeb"}],
                'bar': {'color': "darkred"},}
    ))
  
    gauge.update_layout(paper_bgcolor = "#0f2537", font = {'color': "#ebebeb", 'family': "Arial"})#,margin=dict(l=0, r=0, t=0, b=0))#,width=500,height=300)
    gauge.update_traces(gauge_axis_tickfont_size=15)

    
    n_clicks = None #Set n_clicks back to 0 so it doesnt increment forever
    
    return gauge,date,n_clicks,slider_value



@app.callback(
    Output(component_id="fig_country_capita",component_property="figure"),
    Input(component_id="country_dd",component_property="value"),
    Input(component_id="cummulation_switch",component_property="value")
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
                                "emissions_cumulated":"Kummulierte Emissionen seit 1970 / Gt"}, template=template,
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
                                 template=template,
                                hover_data={"emissions_country":":.2f",
                                            "emissions_capita":":.2f"})
            fig_country_capita.update_layout(yaxis_range=[-1,12.5],xaxis_range=[-1,60])
            fig_country_capita.update_traces(marker_size=9)
            return fig_country_capita

    if on == True:
        # Make plot with all countries if there is no selection
        fig_country_capita = px.scatter(data_frame=emissions,
                                x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",
                                template=template, size="emissions_cumulated",
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
                                x="emissions_capita",y="emissions_country",animation_frame="year",hover_name="Country",template=template,
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
