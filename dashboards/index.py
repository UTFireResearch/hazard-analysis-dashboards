# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import hazard_analysis, vent_calculator


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/hazard_analysis':
        return hazard_analysis.layout
    elif pathname == '/apps/vent_calculator':
        return vent_calculator.layout
    else:
        return html.Div([html.H3('404')])


if __name__ == '__main__':
    app.run_server(debug=True)
