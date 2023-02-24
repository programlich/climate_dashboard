from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

##########
# Colors #
##########
my_color_palette = ["#ffca03",
                    "#ffa011",
                    "#ff7431",
                    "#ff414c",
                    "#f60066",
                    "#d40080",
                    "#660062",
                    "#330a5c",
                    "#5E0B15",
                    "#90323D",
                    "#D9CAB3",
                    "#002642",
                    '#780116',
                    '#F7B538',
                    '#DB7C26',
                    '#8CB369',
                    '#C32F27',
                    '#F4E285',
                    '#D8572A',
                    "#F26157",
                    "#420C14", ]


##########
# Budget #
##########


def create_budget_card(card_header, card_footer, card_style):
    budget_card = dbc.Card([
        dbc.CardHeader([
            html.H2(card_header, style={"textAlign": "center", "display": "inline-block"}),
            html.Div(budget_modal, style={"float": "right", "display": "inline"})
        ]),
        html.Br(),
        dbc.CardBody([
            html.Div(
                daq.Gauge(id="fig_emissions_gauge",
                          showCurrentValue=True,
                          value=200,
                          max=400,
                          min=0,
                          color="#c5860d"
                          ), style={"height": "200px"}
                # for some reason this reduces the unnecessary space between gauge and slider
            )], style={"textAlign": "center", "margin-top": "4px"}),
        html.H3(id="month_budget", style={"textAlign": "center"}),

        html.Div(dcc.Slider(id="gauge_slider", min=1, max=180,
                            marks={1: {"label": "2020", "style": {"font-size": "20px"}},
                                   60: {"label": "2025", "style": {"font-size": "20px"}},
                                   120: {"label": "2030", "style": {"font-size": "20px"}},
                                   180: {"label": "2035", "style": {"font-size": "20px"}}
                                   },
                            updatemode="drag"),  # close slider

                 style={"margin-bottom": "5%",
                        "margin-right": "2%",
                        "margin-left": "2%"}),  # close slider Div

        html.Div(
            dbc.Button("Heute", outline=True, color="danger", id="button_today", n_clicks=0),
            style={"textAlign": "center", "margin-bottom": "5%", }
        ),
        dbc.CardFooter(card_footer, style={"textAlign": "center"})

    ], style=card_style)

    return budget_card


#########################
# Concentration and ssp #
#########################

ssp_checklist = html.Div(
    [
        html.I(className="bi bi-info-circle-fill me-2"),
        dbc.Label("Szenarien", id="popover_scenarios"),

        dbc.Checklist(
            options=[
                {"label": "SSP 1-1.9", "value": "SSP 1-1.9"},
                {"label": "SSP 1-2.6", "value": "SSP 1-2.6"},
                {"label": "SSP 2-4.5", "value": "SSP 2-4.5"},
                {"label": "SSP 3-7.0", "value": "SSP 3-7.0"},
                {"label": "SSP 5-8.5", "value": "SSP 5-8.5"},
            ],
            value=["SSP 1-1.9"],
            id="ssp_checklist",
        ),
        dbc.Popover(
            dcc.Markdown('''SSP steht für *Shared Socio-economic Pathway*
                                und beschreibt Modellszenarien, in denen die 
                                Auswirkungen von Treibhausgasemissionen
                                auf das Klima simuliert werden.    
                                Klicke auf **Info SSP** für mehr Informationen.
                                '''),
            target="popover_scenarios",
            body=True,
            trigger="hover",
        )

    ], style={"margin-bottom": "40px"}
)

ssp_infotext = dcc.Markdown('''
Der [IPCC](https://www.ipcc.ch/) stellt in seinem sechsten Assesment Report ([AR6](https://www.ipcc.ch/assessment-report/ar6/))
fünf Szenarien vor, in denen die Auswirkung unterschiedlich starker
Treibhausgasemissionen auf das Klima modelliert werden.
* **SSP 1-1.9**: Sehr geringe Emissionen, Nettonull ab ca. 2050
* **SSP 1-2.6**: Geringe Emissionen, Nettonull ab ca. 2050 
* **SSP 2-4.5**: Keine Veränderung aktueller Emissionen bis ca. 2050  
* **SSP 3-7.0**: Verdopplung der aktuellen Emissionen bis 2100
* **SSP 5-8.5**: Verdopplung der aktuellen Emissionen bis 2500

**Das 1,5-Grad-Ziel kann nur im Szenario *SSP 1-1.9* mit ausreichend  
hoher Wahrscheinlichkeit (66%)
 erreicht werden.**
                    ''')

ssp_modal = html.Div(
    [
        dbc.Button(html.B("Info SSP"), id="open_ssp_modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Social economic pathway")),
                dbc.ModalBody(ssp_infotext),
                dbc.ModalFooter(
                    dbc.Button(
                        "schließen", id="close_ssp_modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="ssp_modal",
            size="lg",
            is_open=False,
        ),
    ]
)


def create_concentration_card(card_header, card_footer, card_style):
    concentration_card = dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.H2(card_header, style={"textAlign": "center",
                                            "display": "inline-block"}),
                html.Div(concentration_modal, style={"display": "inline-block",
                                                     "float": "right"})
            ], style={"textAlign": "center"})
        ]),

        # Content row
        dbc.Row([
            # Figure col
            dbc.Col([dcc.Graph(id="fig_concentration")], width=10),  # close figure col

            # Menu col
            dbc.Col([
                html.Br(),
                html.Br(),
                ssp_checklist,  # Select certain ssp data
                ssp_modal  # Explanation on ssp
            ], width=2),  # close menu col

        ]),  # close content row
        dbc.CardFooter(card_footer, style={"textAlign": "center"})
    ], style=card_style)  # styling concentration card

    return concentration_card


##############
# Emissions #
##############

def create_emission_tabs(dict_list_countries, app):
    tab_emission = dbc.Row([
        # Open figure col
        dbc.Col([
            dcc.Graph(id="fig_country_capita")
        ], width=10),  # close figure col
        # open menu col
        dbc.Col([
            html.Div([
                dbc.Switch(id="cummulation_switch",
                           value=True,
                           label="Kummulierte Emissionen",
                           style={"margin-bottom": "10px"}),

                dcc.Dropdown(id="country_dd",
                             placeholder="Länder wählen",
                             options=dict_list_countries,
                             multi=True)

            ], style={"margin-top": "13%", "margin-right": "5%"})
        ], width=2)  # close menu col
    ], style={"border": "0.1px #e3e3e3 solid",
              "margin": "2px",
              "border-radius": 10}  # style row
    )  # close row

    top_dd_list = []
    for i in range(1, 209):
        this_dict = {}
        this_dict["label"] = str(i)
        this_dict["value"] = i
        top_dd_list.append(this_dict)

    year_dd_list = []
    for i in range(1970, 2022):
        this_dict = {}
        this_dict["label"] = str(i)
        this_dict["value"] = i
        year_dd_list.append(this_dict)

    tab_emission_toplist = dbc.Row([  # open row

        # open figure col
        dbc.Col([
            dcc.Graph(id="fig_emissions_toplist")
        ], width=10),  # close figure col

        # open menu col
        dbc.Col([
            html.Div([  # buttons div
                dbc.Label("Sortieren nach:", id="popover_emissions_sort"),
                dbc.RadioItems(
                    id="toplist_buttons",
                    options=[
                        {"label": "Land", "value": "emissions_country"},
                        {"label": "Land pro Kopf", "value": "emissions_capita"},
                        {"label": "Kummulierte Emissionen", "value": "emissions_cumulated"},
                    ],
                    value="emissions_country"),

                dbc.Popover(
                    dcc.Markdown(
                        '''Die Rangliste ordnet Länder entsprechend einer von drei möglichen Kategorien an:
* Emissionen in einem bestimmten Jahr
* Pro Kopf Emissionen in einem bestimmten Jahr
* Von 1970 bis zum gewählten Jahr insgesamt ausgestoßene Menge an CO\u2082 (kummulierte Emissionen)
                        '''),
                    target="popover_emissions_sort",
                    body=True,
                    trigger="hover")
            ], style={"margin-top": "10%", "margin-bottom": "20px"}
            ),  # close buttons div

            # Dropdowns
            html.Div("Top"),
            dcc.Dropdown(id="top_dd",
                         placeholder="Top...",
                         options=top_dd_list,
                         value=10,
                         multi=False),
            html.Br(),

            html.Div("Jahr"),
            dcc.Dropdown(id="year_dd",
                         placeholder="Jahr",
                         options=year_dd_list,
                         value=2021,
                         multi=False)

        ], width=2)  # close menu col
    ], style={"border": "0.1px #e3e3e3 solid",  # styling row
              "margin": "2px",
              "border-radius": 10})

    tab_emission_howto = html.Div(dbc.Row([
        # Open figure col
        dbc.Col([

            html.Img(src=app.get_asset_url("explenation_emissions.png"), style={"width": "100%"}),

        ], width=12),  # close image col

    ], style={"border": "0.1px #e3e3e3 solid",
              "margin": "2px",
              "border-radius": 10})  # style row
    )  # close row

    tabs = dbc.Tabs(
        [

            dbc.Tab(tab_emission_toplist, label="Rangliste"),
            dbc.Tab(tab_emission, label="Zeitlicher Verlauf"),
            dbc.Tab(tab_emission_howto, label="Was sehe ich?")

        ]
    )
    return tabs


def create_emission_card(card_header, card_footer, card_style, dict_list_countries, app):
    emission_card = dbc.Card([
        # Header
        dbc.CardHeader([
            html.Div([
                html.H3(card_header, style={"textAlign": "center", "display": "inline-block"}),
                html.Div(emissions_modal, style={"float": "right", "display": "inline-block"})
            ], style={"textAlign": "center"})
        ]),
        # Emissions Content
        # TODO find out why create_emission_tabs needs app as argument and find a more elegant solution
        dbc.CardBody(create_emission_tabs(dict_list_countries, app)),
        dbc.CardFooter(card_footer, style={"textAlign": "center"})
    ], style=card_style)

    return emission_card


####################
# temperature tabs #
####################


def create_temperature_tabs(fig_temp_early, fig_temp_recent):
    tab_temp_early = dbc.Row([dcc.Graph(figure=fig_temp_early, id="fig_temp_early")],
                             style={"border": "0.1px #e3e3e3 solid",  # styling row
                                    "margin": "2px",
                                    "border-radius": 10})

    tab_temp_recent = dbc.Row([dcc.Graph(figure=fig_temp_recent, id="fig_temp_recent")],
                              style={"border": "0.1px #e3e3e3 solid",  # styling row
                                     "margin": "2px",
                                     "border-radius": 10})

    tabs = dbc.Tabs(
        [

            dbc.Tab(tab_temp_recent, label="1850-2019"),
            dbc.Tab(tab_temp_early, label="1-1990")

        ]
    )
    return tabs


###############
# Info modals #
###############

# Budget modal
budget_infotext = dcc.Markdown('''
Der [IPCC](https://www.ipcc.ch/) hat im sechsten Assesment Report ([AR6](https://www.ipcc.ch/assessment-report/ar6/)) ausgerechnet, wie viel CO\u2082 ab Januar 2020
noch in die Atmosphäre gelangen darf, um das 1,5°C Ziel mit einer Wahrscheinlichkeit von 2/3 nicht zu verfehlen.
Diese Menge an CO\u2082 betrug 400 Gigatonnen (Gt).  
Mit den Emissionsdaten aus der [EDGAR](https://edgar.jrc.ec.europa.eu/report_2022)-Datenbank konnte
das emittierte CO\u2082 in den Jahren 2020 und 2021 von diesem Budget abgezogen werden. Die Emissionen für den Zeitraum danach
werden unter der Annahme eines konstanten Ausstoßes berechnet. Dafür werden die dutschnittlichen Emissionen 
aus dem Zeitraum 2015-2021 berechnet(Die Emissionen im Jahre 2020 wurden dabei *nicht* berücksichtigt, da
diese aufgrund der Corona-Pandemie außergewöhnlich niedrig waren).  

Quelle: [IPCC AR6, Tabelle SPM.2](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM_final.pdf#page=33) ''')

budget_modal = html.Div(
    [
        dbc.Button("Info", id="open_budget_modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("CO\u2082 Budget")),
                dbc.ModalBody(budget_infotext),
                dbc.ModalFooter(
                    dbc.Button(
                        "schließen", id="close_budget_modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="budget_modal",
            is_open=False,
        ),
    ]
)

# Concentration modal
concentration_infotext = dcc.Markdown('''
Der [IPCC](https://www.ipcc.ch/) hat im Anhang des sechsten Assesment Report ([AR6](https://www.ipcc.ch/assessment-report/ar6/))
Daten zur CO\u2082-Konzentration in der Atmosphäre seit 1850 veröffentlicht. Diese Daten sind durch die blaue
Kurve (gemessen) dargestellt. Darüber hinaus hat der IPCC Modellszenarien erstellt,
die die künftige CO\u2082-Konzentration in der Atmosphäre unter verschiedenen Randbedingungen 
simuliert. Diese Szenarien werden mit SSP (social economic pathway) und einer Nummer abgekürzt und können durch Auswahl
der einzelnen Checkboxen angezeigt werden.  

Quelle: [IPCC AR6 Annex III](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.pdf)  
Datensatz: [CO\u2082-Konzentration 1850-2020](https://zenodo.org/record/5705391)  
CO\u2082 Konzentration SSPs: [AR6 Annex III](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Annex-III.pdf), Tabelle AIII.2''')

concentration_modal = html.Div(
    [
        dbc.Button("Info", id="open_concentration_modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Atmosphärische CO\u2082-Konzentration")),
                dbc.ModalBody(concentration_infotext),
                dbc.ModalFooter(
                    dbc.Button(
                        "schließen", id="close_concentration_modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="concentration_modal",
            is_open=False,
        ),
    ]
)

# Emission modal
emission_infotext = dcc.Markdown('''
Die europäische Komission stellt in der Datenbank *EDGAR* (Emissions Database for Global Atmospheric Research)
Daten über die weltweiten CO\u2082-Emissionen seit 1970 zur Verfügung. Zur Ermittlung der darin enthaltenen Daten
werden vom IPCC empfohlene [Methoden](https://edgar.jrc.ec.europa.eu/methodology) verwendet.  
Die hier gezeigten Darstellungen wurden auf Basis des Berichts über 
[*CO\u2082 Emissionen aller Länder*](https://edgar.jrc.ec.europa.eu/report_2022) erstellt.
Darin sind Daten zu den Emissionen von 208 einzelnen Ländern seit dem Jahre 1970 enthalten. Die Emissionen werden
sowohl für den Ausstoß pro Land als auch pro Land und Kopf angegeben. Die kummulierten Emissionen wurden für das 
Klimaboard aus den gegebenen Daten berechnet.  

Quelle: [EDGAR 2022](https://edgar.jrc.ec.europa.eu/report_2022)  
[Zum Datensatz](https://edgar.jrc.ec.europa.eu/booklet/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx)  
                        ''')

emissions_modal = html.Div(
    [
        dbc.Button("Info", id="open_emission_modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("CO\u2082-Emissionen")),
                dbc.ModalBody(emission_infotext),
                dbc.ModalFooter(
                    dbc.Button(
                        "schließen", id="close_emission_modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="emission_modal",
            is_open=False,
        ),
    ]
)

# Temperature modal
temp_infotext = dcc.Markdown('''
Die Diagramme zeigen jeweils die Änderung der globalen Oberflächentemperatur relativ zur durchschnittlichen Temperatur von 1850-1900
(vorindustrielles Zeitalter).
* Im Tab **1850-2019** sind Daten abgebildet, welche durch direkte Temperaturmessungen der globalen Oberflächentemperatur ermittelt wurden.
* Die Daten im Tab **1-1995** wurden mit Hilfe der [Paläoklimatologie](https://de.wikipedia.org/wiki/Pal%C3%A4oklimatologie) rekonstruiert. Dafür wurden natürliche Archive wie Baumringe, Eiskernbohrungen, Gestein, etc. untersucht, 
                um Informationen über das Klima in der Vergangenheit zu erhalten. Dies ist ein notwendiges Vorgehen,
                da belastbare Aufzeichnungen über die Oberflächentemperatur der Erde erst ab 1850 existieren.  

Quelle: [IPCC AR6 Figure SMP 1](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM_final.pdf)  
[Zum Datensatz](https://data.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_01/v20210809)
    ''')

temp_modal = html.Div(
    [
        dbc.Button("Info", id="open_temp_modal", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Änderung der globalen Oberflächentemperatur")),
                dbc.ModalBody(temp_infotext),
                dbc.ModalFooter(
                    dbc.Button(
                        "schließen", id="close_temp_modal", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="temp_modal",
            is_open=False,
        ),
    ], style={"float": "right", "display": "inline-block"}
)
