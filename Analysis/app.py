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

from components import ssp_checklist, ssp_modal, create_emission_tabs, create_temperature_tabs

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
dbc_css = os.path.abspath("assets/dbc.min.css")
template = "quartz"

load_figure_template(template)


###############################
## Global temperature change ##
###############################

# Create df for temperature from 1-1990
temp_early = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/temperature_early.csv")
fig_temp_early = px.line(data_frame=temp_early, x="year", y="temp",
    labels={"year":"Jahr","temp":"Temperaturänderung / °C"},width=800)
fig_temp_early.update_layout(xaxis_range=[0,1990],
                            yaxis_range=[-0.2,0.8],
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            modebar = dict(bgcolor='rgba(0, 0, 0, 0)'))
fig_temp_early.update_traces(line_color="#c5860d")
fig_temp_early.update_xaxes(linecolor="white",showgrid=False,zeroline=False)
fig_temp_early.update_yaxes(linecolor="white",showgrid=False,zeroline=False)
   
# Create df for recente temperature changes
temp_recent = pd.read_csv("/home/matthias/Python/Klimadashboard/Analysis/data/temperature_recent.csv")
fig_temp_recent = px.line(data_frame=temp_recent, x="year", y="observed",
    labels={"year":"Jahr","observed":"Temperaturänderung / °C"},width=800)
fig_temp_recent.update_layout(xaxis_range=[1850,2023],yaxis_range=[-0.5,1.5],
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                modebar = dict(bgcolor='rgba(0, 0, 0, 0)'))
fig_temp_recent.update_traces(line_color = "#c5860d")
fig_temp_recent.update_xaxes(linecolor="white",showgrid=False,zeroline=False)
fig_temp_recent.update_yaxes(linecolor="white",showgrid=False,zeroline=False)

# linechart figure for recent temperature changes
fig_temp_line = px.line(data_frame=temp_recent, x="year", y="observed",
 labels={"year":"Jahr","observed":"Temperaturänderung / °C"},
  width=800, template=template)
fig_temp_line.update_layout(xaxis_range=[1850,2023],yaxis_range=[-0.5,1.5])


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
#app = dash.Dash(external_stylesheets=[dbc.themes.MINTY,dbc_css])
app = dash.Dash(__name__)

app.layout = dbc.Container([
            
            # Title row
            dbc.Row(
                #dbc.Col(html.H1("Klimadashboard"),width={"size":6,"offset":3}),
                justify="center",style={"margin-top":"25px"}),
            

            # concentration and budget row
            dbc.Row([
            # Budget col
                dbc.Col([
                        dbc.Card([
                        dbc.CardHeader(html.H2("CO\u2082 Budget / Gt",style={"textAlign":"center"})),
                        html.Br(),
                        dbc.CardBody([
                                daq.Gauge(id ="fig_emissions_gauge",
                                    showCurrentValue=True,
                                    value=200,
                                    max=400,
                                    min=0,
                                    color = "#c5860d"
                                    )],style={"textAlign":"center","margin-top":"4px"}),
                        html.H3(id="month_budget",style={"textAlign":"center"}),

                   
                        html.Div(dcc.Slider(id="gauge_slider",min=1,max=180,
                                marks={ 1:{"label":"2020","style":{"font-size":"20px"}},
                                        60:{"label":"2025","style":{"font-size":"20px"}},
                                        120:{"label":"2030","style":{"font-size":"20px"}},
                                        180:{"label":"2035","style":{"font-size":"20px"}}
                                    },
                                        updatemode="drag"), #close slider

                                style={ "margin-bottom":"5%",
                                        "margin-right":"2%",
                                        "margin-left":"2%"}), #close slider Div
                            
                        html.Div(
                            dbc.Button("Heute",outline=True,color="danger",id="button_today",n_clicks=0),
                            style={"textAlign":"center","margin-bottom":"5%",}
                        )
         
                        ],style={"margin-bottom":"5%",
                                'padding':'0px 0px 8px 0px',
                                "height":"95%"})], #styling budget card
                width={"size":4,"offset":0}), #styling budget col
            # Concentration Column
            dbc.Col(
                # Header
                dbc.Card([
                    dbc.CardHeader(html.H2("CO\u2082 Konzentration in der Atmosphäre",style={"textAlign":"center"})),
                    # Content row
                    dbc.Row([
                        # Figure col    
                        dbc.Col([
                            dcc.Graph(id="fig_concentration")
                            ], width=10), #close figure col
                        
                        # Menu col               
                        dbc.Col([
                            html.Br(),
                            html.Br(),
                            ssp_checklist, #Select certain ssp data
                            ssp_modal      #Explenation on ssp     
                            ], width=2), #close menu col

                            ]) #close content row
                        
                ],style={"height":"95%"} #styling concentration
                ), #close concentration card
                width=8), #close concentration col


                

            ],style={"margin-bottom":"0px"}), #close concentration and budget row


            # Emissions row  
            dbc.Card([
                # Header
                dbc.CardHeader(html.H2("CO\u2082 Emissionen durch Verbrennung fossiler Energieträger",
                                style={"textAlign":"center"})),
                # Emissions Content
                dbc.CardBody(create_emission_tabs(dict_list_countries),
                            )
                    ],style={"margin-bottom":"2%"}
                    ),




               
  

            # Temperature row
            dbc.Row([
                # First col
                dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H2("Änderung der globalen Oberflächentemperatur relativ zum Zeitraum 1850-1900")),
                #dcc.Graph(figure=fig_temp_recent,id="kdfa")
                dbc.CardBody(
                create_temperature_tabs(fig_temp_early,fig_temp_recent)
                             )   ])

                    ],style={"margin-bottom":"30px"},width={"size":10,"offset":1}), # Close first row
       
            
                ]) #close dbc containe2 

],className="dbc")

# Callback for CO2 concentration
@app.callback(Output(component_id="fig_concentration",component_property="figure"),
              Input(component_id="ssp_checklist",component_property="value")
)

def plot_concentration(checked):
    concentration_copy = concentration.copy(deep=True)
    
    show_list = ["gemessen"] + checked  #Select all lines to be shown

    # Select all the corresponding colors to the selected data
    color_dict = {"value":["gemessen","ssp119",'ssp126','ssp245','ssp370','ssp585'],
            "color":["#aba7a7","#c5860d","#ba640c","#f44336","#ae2a12","#821f33"]}
    color_df = pd.DataFrame(color_dict)
    color_list = []
    for line in show_list:
        color_list.append(color_df.loc[color_df["value"]==line,"color"].item())
    
    # Create line chart 
    fig = px.line(data_frame=concentration_copy,x="year",y=show_list, color_discrete_sequence=color_list,
                 labels={"value":"CO\u2082 Konzentration / ppm","year":"Jahr","variable":""})
    fig.update_xaxes(linecolor = "white")
    fig.update_yaxes(linecolor = "white")
    fig.update_traces(hovertemplate=None,line_width = 3)
    fig.update_layout(font_size = 14,
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    modebar = dict(bgcolor='rgba(0, 0, 0, 0)'))
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


# Callback for Capita Country Emissions
@app.callback(
    Output(component_id="fig_country_capita",component_property="figure"),
    Input(component_id="country_dd",component_property="value"),
    Input(component_id="cummulation_switch",component_property="value")
)
def update_figure(selection,cumulated_on):

    emissions = emissions_inverted_merged.copy(deep=True)
    color = None
    # Show different plot if countries are selected
    if selection:
        color = "Country"
        selection_list = selection

        # Select only the emission data about the selected countries
        emissions = emissions.loc[emissions["Country"].isin(selection_list),:]

        if cumulated_on==True:
            # Make the plot
            size = "emissions_cumulated"

            
        elif cumulated_on == False:
            # Make the plot
            size = None

            
    if cumulated_on == True:
        # Make plot with all countries if there is no selection
        size = "emissions_cumulated"

        
    else:
        # Make plot with all countries if there is no selection
        size = None
        
    
    # Create the plot with the selected parameters
    fig_country_capita = px.scatter(data_frame=emissions,
                                x="emissions_capita",
                                y="emissions_country",
                                animation_frame="year",
                                hover_name="Country",
                                size = size,
                                color = color,
                                template="ggplot2",
                                labels={"emissions_country": "Land / Gt ",
                                         "emissions_capita":'Land pro Kopf / t ',
                                         "emissions_cumulated":"Kummuliert / Gt",
                                         "year":"Jahr "},
                                hover_data={"emissions_country":":.2f",
                                            "emissions_capita":":.2f",
                                            "emissions_cumulated":":.2f"})
    
    fig_country_capita.update_xaxes(showline = False,zerolinecolor="white",showgrid=False)
    fig_country_capita.update_yaxes(showline=False,zerolinecolor="white",showgrid=False)
    fig_country_capita.update_layout(yaxis_range=[-1,13.5],xaxis_range=[-1,60],
                                    font_size = 14,
                                    font_color = "white",
                                    template = None,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    modebar = dict(bgcolor='rgba(0, 0, 0, 0)'))
    fig_country_capita.update_traces(marker_size=10)
    return fig_country_capita

# Callback for emissions toplist
@app.callback(Output(component_id="fig_emissions_toplist",component_property="figure"),
              Input(component_id="toplist_buttons",component_property="value"),
              Input(component_id="top_dd",component_property="value"),
              Input(component_id="year_dd",component_property="value")
)

def update_emissions_toplist(top_type,top_number,top_year):

    emissions = emissions_inverted_merged.copy(deep=True)

    # Sort and slice emissions according to user input
    emissions = emissions.loc[emissions["year"] == top_year,:]
    emissions = emissions.sort_values(by=[top_type],ascending=False)
    emissions = emissions.head(top_number)

    fig = px.scatter(data_frame=emissions,
                     x="emissions_capita",
                     y="emissions_country",
                     size="emissions_cumulated",
                     color="Country",
                     hover_name="Country",
                     template=template,
                     labels={"emissions_country": "Land / Gt ",
                                "emissions_capita":'Land pro Kopf / t ',
                                "emissions_cumulated":"Kummuliert / Gt",
                                "year":"Jahr "},
                     hover_data={"emissions_country":":.2f",
                                "emissions_capita":":.2f",
                                "emissions_cumulated":":.2f"})
    
    fig.update_xaxes(showline = False,zerolinecolor="white",zeroline=True,gridcolor="#accbe6")
    fig.update_yaxes(showline = False,zerolinecolor="white",zeroline=True,gridcolor="#accbe6")
    fig.update_layout(font_size = 14,
                    yaxis = dict(rangemode = 'tozero'),
                    xaxis = dict(rangemode = 'tozero'),
                    font_color = "white",
                    template = None,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    modebar = dict(bgcolor='rgba(0, 0, 0, 0)'))
    fig.update_traces(marker_line_width=0)
    return fig
    

    
    

if __name__=="__main__":
    app.run_server(debug=True)
