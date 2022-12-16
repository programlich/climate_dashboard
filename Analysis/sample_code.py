 """        # Div for temp bar graph and slider
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

                ], 
            style={"display":"inline-block", "width":"30%", "margin":"10px auto"})

            ] 
             """
""" app.layout = html.Div(children=[
    
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
            html.Div(daq.BooleanSwitch(id="cummulation_switch",
                            on=False,
                            label="Kummulierte Emissionen",
                            labelPosition="right",
                            style={"width":"25%","margin":"auto",
                                "display":"block"}
                            )
                    ),
            
            html.Div(
                dcc.Dropdown(id="country_dd",
                        options=dict_list_countries,
                        multi=True,
                        style={"width":"45%","margin":"10px auto"}) 
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

        ])  # Close global div """

""" daq.Gauge( 
                            id = "gauge",
                            color={"gradient":True,"ranges":{"green":[0,133],"yellow":[133,266],"red":[266,400]}},
                            value=300,
                            max=400,
                            min=0,
                            scale={'custom':{'0':{'label':'0', 'style':{'font-size':'20px'}},
                                            '100':{'label':'100', 'style':{'font-size':'20px'}},
                                            '200':{'label':'200', 'style':{'font-size':'20px'}},
                                            '300':{'label':'300', 'style':{'font-size':'20px'}},
                                            '400':{'label':'400', 'style':{'font-size':'20px'}},
                                            }
                                    },                            
                                ) """

tab_emission = html.Div([
                    dbc.Col([
                    dcc.Graph(id="fig_country_capita")
                    ],width=10), #close figure col
                
                dbc.Col([
                    dbc.Switch( id="cummulation_switch",
                                value=False,
                                label="Kummulierte Emissionen",
                                style={"margin-bottom":"10px"}),
                    
                    dcc.Dropdown(id="country_dd",
                                 options=dict_list_countries,
                                 multi=True)

                    ],width=2) #close menu col    
                ])