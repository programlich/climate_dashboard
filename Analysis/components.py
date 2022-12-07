from dash import html
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



