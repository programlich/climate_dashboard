import plotly.express as px


def create_fig_temp_early(data_temp_early):
    fig_temp_early = px.line(data_frame=data_temp_early, x="year", y="temp",
                             labels={"year": "Jahr", "temp": "Temperaturänderung / °C"},
                             width=800)
    fig_temp_early.update_layout(xaxis_range=[0, 1990],
                                 yaxis_range=[-0.2, 0.8],
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)',
                                 modebar=dict(bgcolor='rgba(0, 0, 0, 0)'))
    fig_temp_early.update_traces(line_color="#c5860d")
    fig_temp_early.update_xaxes(linecolor="white", showgrid=False, zeroline=False)
    fig_temp_early.update_yaxes(linecolor="white", showgrid=False, zeroline=False)

    return fig_temp_early


def create_fig_temp_recent(data_temp_recent):
    fig_temp_recent = px.line(data_frame=data_temp_recent, x="year", y="observed",
                              labels={"year": "Jahr", "observed": "Temperaturänderung / °C"},
                              width=800)
    fig_temp_recent.update_layout(xaxis_range=[1850, 2023], yaxis_range=[-0.5, 1.5],
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  modebar=dict(bgcolor='rgba(0, 0, 0, 0)'))
    fig_temp_recent.update_traces(line_color="#c5860d")
    fig_temp_recent.update_xaxes(linecolor="white", showgrid=False, zeroline=False)
    fig_temp_recent.update_yaxes(linecolor="white", showgrid=False, zeroline=False)

    return fig_temp_recent
