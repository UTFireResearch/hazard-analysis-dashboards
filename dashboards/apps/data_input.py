# # -*- coding: utf-8 -*-

from collections import defaultdict

import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps.util import FLAMMABILITY_COLLECTION, MAIN_COLLECTION, parse_contents
from db.api import find, insert_data


layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value="data-entry",
        children=[
            dcc.Tab(
                label="Data Entry",
                value="data-entry",
                children=[
                    html.Div([
                        html.Label(
                            [
                                '*Publication:',
                                dcc.Input(
                                    id="publication_input",
                                    placeholder="Last Name, Year",
                                    required=True,
                                    className="control_label",
                                ),
                            ],
                            className="control_label",
                            style={
                                'width': '25%',
                                "margin-top": "15px"
                            }
                        ),
                        html.Label(
                            [
                                'Cell type:',
                                dcc.Input(
                                    id="cell_type_input",
                                    className="control_label"
                                ),
                            ],
                            className="control_label",
                            style={
                                'width': '25%',
                                "margin-top": "15px"
                            }
                        ),
                        html.Label(
                            [
                                'Chemistry:',
                                dcc.Input(
                                    id="chemistry_input",
                                    className="control_label",
                                ),
                            ],
                            className="control_label",
                            style={
                                'width': '25%',
                                "margin-top": "15px"
                            }
                        ),
                        html.Label(
                            [
                                'Electrolyte:',
                                dcc.Input(
                                    id="electrolyte_input",
                                    className="control_label",
                                ),
                            ],
                            className="control_label",
                            style={
                                'width': '25%',
                                "margin-top": "15px"
                            }
                        ),
                        html.Label(
                            [
                                'SOC:',
                                dcc.Input(
                                    id="soc_input",
                                    className="control_label",
                                ),
                            ],
                            className="control_label",
                            style={
                                'width': '25%',
                                "margin-top": "15px"
                            }
                        ),
                        html.Div(
                            [
                                html.Label(
                                    [
                                        'CO2:',
                                        dcc.Input(
                                            id="co2_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'CO:',
                                        dcc.Input(
                                            id="co_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'H2:',
                                        dcc.Input(
                                            id="h2_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'CH4:',
                                        dcc.Input(
                                            id="ch4_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'C2H4:',
                                        dcc.Input(
                                            id="c2h4_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'C2H6:',
                                        dcc.Input(
                                            id="c2h6_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'C3H8:',
                                        dcc.Input(
                                            id="c3h8_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'N2:',
                                        dcc.Input(
                                            id="n2_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'O2:',
                                        dcc.Input(
                                            id="o2_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'CH3OH:',
                                        dcc.Input(
                                            id="ch3oh_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                                html.Label(
                                    [
                                        'Other:',
                                        dcc.Input(
                                            id="other_input",
                                            type="number",
                                            min=0,
                                            placeholder=0.0,
                                            className="control_label",
                                        ),
                                    ],
                                    className="control_label",
                                    style={'width': '10%'}
                                ),
                            ],
                            className="row",
                            style={
                                "margin-top": "15px"
                            }
                        ),
                        html.Div(
                            [
                                html.Label(
                                    [
                                        '*Upload File:',
                                        dcc.Upload(
                                            id='upload-data',
                                            children=html.Div([
                                                'Drag and Drop or ',
                                                html.A('Select File')
                                            ]),
                                            style={
                                                'width': '90%',
                                                'height': '60px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin': '10px'
                                            },
                                            # Don't allow multiple uploads
                                            multiple=False
                                        ),
                                    ],
                                    className="control_label",
                                    style={"margin-top": "15px"}
                                ),
                                html.Div(id='output-data-upload'),
                            ],
                        ),
                        html.Div(
                            [
                                html.Button("SUBMIT ENTRY",
                                            id="submit_entry")
                            ],
                            style={
                                "margin-left": "10px",
                                "margin-top": "20px"
                            }
                        ),
                    ], className="input__container",
                    ),
                ]
            ),
            dcc.Tab(
                label="View Data",
                value="view-data",
                children=[
                    html.Div([
                        html.Div([
                            dash_table.DataTable(
                                id="entry-table",
                                fixed_rows={'headers': True, 'data': 0},
                                style_cell={
                                    "minWidth": "0px",
                                    "maxWidth": "180px",
                                    "maxHeight": "600px",
                                    "whiteSpace": "normal",
                                    'textAlign': 'center'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                                style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'
                                }
                            )
                        ], className="table__1")
                    ], className="table__container"),
                ]
            )
        ], className="tabs__container")],
    className="pretty_container column",
)


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(content, name, date):
    """ Update uploaded data table. """
    if content is not None:
        children = [parse_contents(content, name, date)]
        return children


@app.callback(
    Output("tabs", "value"),
    [Input("submit_entry", "n_clicks")],
    [
        State("publication_input", "value"),
        State("cell_type_input", "value"),
        State("chemistry_input", "value"),
        State("electrolyte_input", "value"),
        State("soc_input", "value"),
        State("co2_input", "value"),
        State("co_input", "value"),
        State("h2_input", "value"),
        State("ch4_input", "value"),
        State("c2h4_input", "value"),
        State("c2h6_input", "value"),
        State("c3h8_input", "value"),
        State("n2_input", "value"),
        State("o2_input", "value"),
        State("ch3oh_input", "value"),
        State("other_input", "value"),
        State("upload_table", "data"),
    ],
)
def entry_to_db(submit_entry, publication, cell_type, chemistry, electrolyte,
                soc, co2, co, h2, ch4, c2h4, c2h6, c3h8, n2, o2, ch3oh, other,
                data_table):
    """ Submit data to the database. """
    if submit_entry and publication and data_table:
        author, year = [s.strip() for s in publication.split(',')]
        row = {
            'A-hr': '',
            'Author': author,
            'Chemistry': chemistry or '',
            'Electrolyte': electrolyte or '',
            'Failure': '',
            'Format': cell_type or '',
            'GasVol': '',
            'Gases': {'(CH3)2C6H4': 0,
                      'C2H2': 0,
                      'C2H4': c2h4 or 0,
                      'C2H5F': 0,
                      'C2H5OH': 0,
                      'C2H6': c2h6 or 0,
                      'C3H6': 0,
                      'C3H8': c3h8 or 0,
                      'C4H10': 0,
                      'C4H102': 0,
                      'C4H8': 0,
                      'C5H12': 0,
                      'C5H123': 0,
                      'C6H6': 0,
                      'C7H8': 0,
                      'C8H10': 0,
                      'CH3F': 0,
                      'CH3OCH3': 0,
                      'CH3OCHO': 0,
                      'CH3OH': ch3oh or 0,
                      'CH4': ch4 or 0,
                      'CO': co or 0,
                      'CO2': co2 or 0,
                      'H2': h2 or 0,
                      'N2': n2 or 0,
                      'O2': o2 or 0,
                      'Other': other or 0,
                      'PF3': 0,
                      'THC': 0},
            'L/Wh': '',
            'Mass': '',
            'Notes': '',
            'Pmax': '',
            'Publication': publication,
            'SOC': soc or '',
            'Voltage': '',
            'W-hr': '',
            'Year': year}
        insert_data(MAIN_COLLECTION, row)

        # Clean up uploaded data
        headers = list(data_table[0].keys())
        headers.remove('Unnamed: 0')  # Remove 'Unnamed: 0' header
        columns = defaultdict(list)
        for item in data_table:
            for header in headers:
                columns[header].append(item[header])

        attrs = [author, year, chemistry, soc]
        _id = []
        for value in attrs:
            value = str(value)
            value = value.lower()
            value = value.replace(',', '')
            _id.append('-'.join(value.split()))
        columns['_id'] = '-'.join(_id)

        insert_data(FLAMMABILITY_COLLECTION, dict(columns))

        return "view-data"

    raise PreventUpdate


@app.callback([
    Output("entry-table", "columns"),
    Output("entry-table", "data")],
    [Input("tabs", "value")],
)
def entry_table(tab):
    """ Render data table. """
    if tab == "view-data":
        data = list(find(MAIN_COLLECTION, projection={'_id': 0}))
        for dct in data:
            dct.pop('Author')
            dct.pop('Year')
            gases = dct.pop('Gases')
            for gas, value in gases.items():
                dct[gas] = value
        columns = [{"name": i, "id": i} for i in data[0].keys()]

        return columns, data

    raise PreventUpdate
