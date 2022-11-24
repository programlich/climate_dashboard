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
        
        # Div for temp bar graph and slider
        html.Div([
        
        # Temp bar graph
        html.Div(dcc.Graph(id="fig_temp_bar"),
            style={"display":"inline-block","margin":"1px",
                    "width":"80%"}),
        # Time slider    
        html.Div(dcc.Slider(id="year_slider", updatemode='drag',
                min=1850, max=2019, value=1850,vertical=False,
                 tooltip={"placement":"top","always_visible":True}),
            style={"display":"block","margin":"1px",
                    "width":"80%","padding":"0px,0px,0px,0px"})

                ], style={"display":"inline-block", "width":"30%", "margin":"10px auto"})

            ])],

        # Styling first row
        style={'width':'90%','margin':"10px auto", 
                        "border":"2px solid green"}
        )
                        


        
@app.callback(
    Output(component_id="fig_temp_bar",component_property="figure"),
    Input(component_id="year_slider",component_property="value")
)

def update_bar_temp(selection):
    year = 1850
    if selection:
        year = selection
    fig_temp_bar = px.bar(data_frame=temp_recent, x=temp_recent.loc[temp_recent["year"]==year,
            "year"],y=temp_recent.loc[temp_recent["year"]==year,"observed"],width=400,
            labels={"x":"Jahr","y":"Temperaturänderung / °C"})
    fig_temp_bar.update_xaxes(visible=False)
    fig_temp_bar.update_layout(yaxis_range=[0,1.6])
    return fig_temp_bar



if __name__=="__main__":
    app.run_server(debug=True)



""" 

    
        
        # First line elements
        html.Div([
            html.Div(
                style={"width":"20%",'height':'20%',
                "background-color":"blue",'display':'inline-block',
                "margin":"50px auto","padding":"10px"}),
            html.Div(
                style={'width':'20%','height':'20%',
                'background-color':"red", 'display':'inline-block',
                "margin":"50px auto"})],
            style={"width":"80%", "height":"80px",
                    "border":"3px dotted yellow",
                    "background-color":"black",
                    "margin":"10px auto", "display":"block"})
            
    
        ],
    # Global div styling
    style={"background-color":"lightgreen"}) """