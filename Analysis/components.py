from dash import html, dcc
import dash_bootstrap_components as dbc



ssp_checklist = html.Div(
    [
        html.I(className="bi bi-info-circle-fill me-2"),
        dbc.Label("Szenarien",id="pop1"),
        
        dbc.Checklist(
            options=[
                {"label": "ssp119", "value": "ssp119"},
                {"label": "ssp126", "value": "ssp126"},
                {"label": "ssp245", "value": "ssp245"},
                {"label": "ssp370", "value": "ssp370"},
                {"label": "ssp585", "value": "ssp585"},
            ],
            value=["ssp119"],
            id="ssp_checklist",
        ),
        dbc.Popover(
            "ssps sind irgendwas vom ipcc. Klicke auf 'Was sind ssps für weitere Infos'",
            target="pop1",
            body=True,
            trigger="hover",
        )

    ],style={"margin-bottom":"40px"}
)

ssp_infotext = "lorem ipsum"

ssp_modal = html.Div(
    [
        dbc.Button("Info ssp", id="open_ssp_modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Social pathway")),
                dbc.ModalBody(ssp_infotext),
                dbc.ModalFooter(
                    dbc.Button(
                        "schließen", id="close_ssp_modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="ssp_modal",
            is_open=False,
        ),
    ]
)


def create_emission_tabs(dict_list_countries):
   
    
    tab_emission =  dbc.Row([
                            # Open figure col
                            dbc.Col([
                            dcc.Graph(id="fig_country_capita")
                                    ],width=10), #close figure col
                            # open menu col
                            dbc.Col([
                            html.Div([
                            dbc.Switch( id="cummulation_switch",
                                    value=False,
                                    label="Kummulierte Emissionen",
                                    style={"margin-bottom":"10px"}),
                        
                            dcc.Dropdown(id="country_dd",
                                        placeholder = "Länder wählen",
                                        options=dict_list_countries,
                                        multi=True)

                            ],style={"margin-top":"13%","margin-right":"5%"})
                            ] ,width=2) #close menu col    
                    ], style={  "border":"0.1px #e3e3e3 solid",
                                "margin":"2px",
                                "border-radius":10} #style row
                    ) #close row

    top_dd_list = []
    for i in range(1,209):
        this_dict = {}
        this_dict["label"] = str(i)
        this_dict["value"] = i
        top_dd_list.append(this_dict)

    year_dd_list = []
    for i in range(1970,2022):
        this_dict = {}
        this_dict["label"] = str(i)
        this_dict["value"] = i
        year_dd_list.append(this_dict)

    tab_emission_toplist =  dbc.Row([ #open row
                
                #open figure col
                dbc.Col([
                    dcc.Graph(id="fig_emissions_toplist")
                    ],width=10), #close figure col
                
                #open menu col
                dbc.Col([
                    html.Div([  #buttons div
                        dbc.Label("Sortieren nach:"),
                        dbc.RadioItems(
                            id="toplist_buttons",
                            options=[
                                {"label": "Land", "value": "emissions_country"},
                                {"label": "Land pro Kopf", "value": "emissions_capita"},
                                {"label": "Kummulierte Emissionen", "value": "emissions_cumulated"},
                            ],
                            value="emissions_country"),
                        ],style={"margin-top":"10%","margin-bottom":"20px"}
                    ), #close buttons div
                                
                    # Dropdowns
                    html.Div("Top"),    
                        dcc.Dropdown(id="top_dd",
                                 placeholder = "Top...",
                                 options=top_dd_list,
                                 value = 10,
                                 multi=False),
                    html.Br(),
                    
                    html.Div("Jahr"),
                        dcc.Dropdown(id="year_dd",
                                 placeholder = "Jahr",
                                 options=year_dd_list,
                                 value = 2020,
                                 multi=False)

                    ],width=2) #close menu col    
                ],style={"border":"0.1px #e3e3e3 solid",    #styling row
                        "margin":"2px",
                        "border-radius":10})

    tabs = dbc.Tabs(
    [
    
    dbc.Tab(tab_emission_toplist, label="Rangliste"),
    dbc.Tab(tab_emission, label="Emissionen")
    
    ]
        )
    return tabs


####################
# temperature tabs #
####################


def create_temperature_tabs(fig_temp_early, fig_temp_recent):

    tab_temp_early = dbc.Row([ dcc.Graph(figure=fig_temp_early,id="fig_temp_early") ],
                            style={"border":"0.1px #e3e3e3 solid",    #styling row
                                    "margin":"2px",
                                    "border-radius":10})

    tab_temp_recent = dbc.Row([ dcc.Graph(figure=fig_temp_recent,id="fig_temp_recent") ],
                            style={"border":"0.1px #e3e3e3 solid",    #styling row
                                    "margin":"2px", 
                                    "border-radius":10})

    tabs = dbc.Tabs(
    [
    
    dbc.Tab(tab_temp_recent, label="1850-2019"),
    dbc.Tab(tab_temp_early, label="1-1990")
    
    ]
        )
    return tabs