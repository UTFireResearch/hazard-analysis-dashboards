# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import data_input, hazard_analysis, explosion_calculator, vent_calculator, incident_map, table, t_squared, mesh_size, HGL_temp, steel_heating, react_balance, flame_size

app.title = 'Hazard Tools'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/hazard_analysis':
        return hazard_analysis.layout
    elif pathname == '/apps/explosion_calculator':
        return explosion_calculator.layout
    elif pathname == '/input':
        return data_input.layout
    elif pathname == '/apps/vent_calculator':
        return vent_calculator.layout
    elif pathname == '/apps/incident_map':
        return incident_map.layout
    elif pathname == '/apps/table':
        return table.layout
    elif pathname == '/apps/t_squared':
        return t_squared.layout
    elif pathname == '/apps/mesh_size':
        return mesh_size.layout
    elif pathname == '/apps/flame_size':
        return flame_size.layout
    elif pathname == '/apps/steel_heating':
        return steel_heating.layout
    elif pathname == '/apps/reaction_balancer':
        return react_balance.layout
    elif pathname == '/apps/HGL_temp':
        return HGL_temp.layout
    else:
        return html.Div([html.H3('404')])


if __name__ == '__main__':
    app.run_server(debug=True)
