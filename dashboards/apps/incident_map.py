import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import math
import copy
import json
import datetime as dt


from app import app
from .callbacks import * #noqa
from .controls import plot_layout, APPLICATIONS, INCIDENTS
from .util import get_incident_data_lean

mapbox_access_token = 'pk.eyJ1Ijoic21hdHRoZXdzOTUiLCJhIjoiY2tnOXZ6bHI2MDE3YTJybXVnZTlmZHQ2aiJ9.4-K3Y_0bc4Z-KJVwNn-TkA'

MASTER_DATAFRAME = None
FILTERED_DATAFRAME = None

main_map_layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Incident Map",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=0, lat=0),
        zoom=0.9,
    ),
)

application_options = [
    {"label": str(APPLICATIONS[application]), "value": str(application)}
    for application in APPLICATIONS
]

incident_options = [
    {"label": str(INCIDENTS[type]), "value": str(type)}
    for type in INCIDENTS
]

YEAR_RANGE = [2006,2021]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

DATA_LAYOUT= html.Div(
    [

    ]
)

#------------------------CONTAINER FOR WHOLE LAYOUT
layout = html.Div(
    [   #-----------------------HEADER BAR DIV---------------------------------
        html.Div(
            [   #---------------------LEFT HEADER COLUMN-----------------------
                html.Div(
                    [   #-----------------UT LOGO------------------------------
                        html.Img(
                            src=("/assets/shield.png"),
                            style={
                                "height": "60px",
                                "width": "auto",
                                "textAlign": 'center',
                            }
                        )
                    ],
                    id="logo",
                    style={'textAlign': 'left'},
                    className='one-third column',
                ),
                #---------------------CENTER HEADER COLUMN---------------------
                html.Div(
                    [   #-------------------HEADER TITLE-----------------------
                        html.H3(
                            'Battery Fire and Explosion Incidents:',
                            style={'margin-bottom': '5px'}
                        ),
                        html.H6(
                            'Database Tools',
                            style={'margin': '0px'}
                        )
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "5px", "margin-top": "5px",'textAlign': 'center'}
                ),
                #--------------------LEGACY NAVIGATION BUTTONS-----------------
                #---------------------RIGHT HEADER COLUMN----------------------
                html.Div(
                    [
                        # html.A(
                        #     html.Button("Building Deflagration",
                        #                 id="building-deflagration",
                        #                 style={'width': '100%'}
                        #     ),
                        #     href="/apps/explosion_calculator",
                        #     style={"float": "right", 'width': '250px'}
                        # ),
                        # html.A(
                        #     html.Button("Vent Sizing",
                        #                 id="vent-sizing",
                        #                 style={'width': '100%'}
                        #     ),
                        #     href="/apps/vent_calculator",
                        #     style={"float": "right","width": '250px'}
                        # ),
                        html.A(
                            html.Button("Tools Home",
                                        id="building-deflagration",
                                        style={'width':'100%'}
                            ),
                            href='/apps/table',
                            style={"float": "right", "width": "240px"}
                        ),
                    ],
                    className="one-third column",
                    id="button",
                    style={'margin-right': '10px'}
                ),
            ],
            id="header",
            className='row flex-display',
            style={
                "margin-bottom": "30px"
            }
        ), #-----------------------END HEADER DIV------------------------------

        #--------------------------FIRST CONTENT ROW----------------------------
        html.Div(
            [   #--------------------DATA HOLDER--------------------------------
                html.Div(
                    id='incident_data',
                    children=get_incident_data_lean(),
                    style={'display':'none'}
                    ),
                #------------FILTER OPTIONS PRETTY CONTAINER---------------------
                html.Div(
                    [
                        html.P('Filter by incident date (or select range in histogram):'),
                        dcc.RangeSlider(
                            id="year_slider",
                            min= YEAR_RANGE[0],
                            max= YEAR_RANGE[1],
                            value=YEAR_RANGE,
                            className="dcc_control"
                        ),
                        html.Hr(style={'margin-bottom': '10px', 'margin-top': '10px'}),
                        html.P('Filter by battery application:'),
                        dcc.RadioItems(
                            id='application_type_selector',
                            options=[
                                {'label': 'All Applications', 'value': 'all'},
                                {'label': 'Customize', 'value': 'custom'}
                            ],
                            value='all',
                            labelStyle={'display': 'inline-block'},
                            className='dcc_control',
                        ),
                        dcc.Dropdown(
                            id='application_types',
                            options=application_options,
                            multi=True,
                            value=list(APPLICATIONS.keys()),
                            className='dcc_control',
                        ),
                        html.Hr(style={'margin-bottom': '10px', 'margin-top': '10px'}),
                        html.P('Filter by incident type:'),
                        dcc.Dropdown(
                            id='incident_types',
                            options=incident_options,
                            multi=True,
                            value=list(INCIDENTS.keys()),
                            className='dcc_control'
                        ),

                    ],
                    id='cross-filter-options',
                    className='pretty_container four columns',
                ),
                #-------------FIRST CONTENT ROW (SECOND COLUMN)----------------
                html.Div(
                    [
                        #----------------MINI-CONTAINER ROW--------------------
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(id='iNumber', children='1000'),
                                        html.P('No. of Incidents'),
                                    ],
                                    id='incident_number',
                                    className='mini_container',
                                ),
                                # html.Div(
                                #     [
                                #         html.H6(id='fNumber', children='1000'),
                                #         html.P('No. of Fires'),
                                #     ],
                                #     id='fire_number',
                                #     className='mini_container',
                                # ),
                                html.Div(
                                    [
                                        html.H6(id='kNumber', children='1000'),
                                        html.P('No. of Deaths'),
                                    ],
                                    id='killd_number',
                                    className='mini_container',
                                ),
                                html.Div(
                                    [
                                        html.H6(id='hNumber', children='1000'),
                                        html.P('No. of Injuries'),
                                    ],
                                    id='hurt_number',
                                    className='mini_container',
                                ),
                                # html.Div(
                                #     [
                                #         html.H6(id='yMax', children='1000'),
                                #         html.H6(id='yMin', children='1000'),
                                #     ],
                                #     id='slider-test',
                                #     className='mini_container',
                                # ),
                                # html.Div(
                                #     [
                                #         html.H6(id='sMax', children='1000'),
                                #         html.H6(id='sMin', children='1000'),
                                #     ],
                                #     id='graph-test',
                                #     className='mini_container',
                                # ),
                            ],
                            id='info-container',
                            className='row container-display',
                            style={'display': 'flex','position': 'relative'},
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="count_graph", style={'autosize':'true'})
                            ],
                            id='countGraphContainer',
                            className='pretty_container',
                        ),
                    ],
                    id='right-column',
                    className='eight columns'

                ),
            ],
            id="second_row",
            className="row flex-display",
            style={"margin-bottom": "25px"}
        ),
        #-------------------SECOND CONTENT ROW---------------------------------
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="map_graph")
                    ],
                    className="pretty_container eight columns",
                    style={'dispaly': 'flex', 'alignItems': 'center'}
                ),
                html.Div(
                    [
                        html.H6(
                            id='incident_info_header',
                            children='Incident Information',
                            style={'textAlign': 'center'}
                        ),
                        html.P(
                            '(Click on map points)',
                            style={'textAlign': 'center'}
                        ),
                        html.Hr(
                            style={'margin-top': '10px', 'margin-bottom': '10px'}
                        ),
                        html.Div(
                            [   html.Div(
                                    [
                                            html.P(
                                                children='Date:',
                                                style={'float':'left'}
                                            ),
                                    ],
                                    className='one-half column'
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            id='info_date',
                                            children='----',
                                            style={'float':'right'},
                                        ),
                                    ],
                                    className='one-half column'
                                ),
                            ],
                            className='row flex-display',
                        ),
                        html.Hr(
                            style={'margin-top': '10px', 'margin-bottom': '10px'}
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            children='Location:',
                                            style={'textAlign': 'left'}
                                        ),
                                    ],
                                    className='one-half column'
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            id='info_place',
                                            children='----',
                                            style={'textAlign':'right'}
                                        )
                                    ],
                                    className='one-half column'
                                ),
                            ],
                            className='row flex-display',
                        ),
                        html.Hr(
                            style={'margin-top': '10px', 'margin-bottom': '10px'}
                        ),
                        html.Div(
                            [   html.Div(
                                    [
                                        html.P(
                                            children='Application:',
                                            style={'textAlign': 'left'}
                                        ),
                                    ],
                                    className='one-half column',
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            id='info_application',
                                            children='----',
                                            style={'textAlign':'right'}
                                        ),
                                    ],
                                    className='one-half column',
                                ),
                            ],
                            className='row flex-display',
                        ),
                        html.Hr(
                            style={'margin-top': '10px', 'margin-bottom': '10px'},
                        ),
                        html.Div(
                            [   html.Div(
                                    [
                                        html.P(
                                            children='Injured:',
                                            style={'textAlign': 'left'}
                                        ),
                                    ],
                                    className='one-half column',
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            id='info_injured',
                                            children='----',
                                            style={'textAlign':'right'}
                                        ),
                                    ],
                                    className='one-half column',
                                ),
                            ],
                            className='row flex-display',
                        ),
                        html.Hr(
                            style={'margin-top': '10px', 'margin-bottom': '10px'},
                        ),
                        html.Div(
                            [   html.Div(
                                    [
                                        html.P(
                                            children='Killed:',
                                            style={'textAlign': 'left'}
                                        ),
                                    ],
                                    className='one-half column',
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            id='info_killed',
                                            children='----',
                                            style={'textAlign':'right'}
                                        ),
                                    ],
                                    className='one-half column',
                                ),
                            ],
                            className='row flex-display',
                        ),
                        html.Hr(
                            style={'margin-top': '10px', 'margin-bottom': '10px'},
                        ),
                        html.Div(
                            [
                                html.P(
                                    children='Description:',
                                    style={'textAlign': 'left'}
                                ),
                            ],
                            className='row flex-display'
                        ),
                        html.Div(
                            [
                                html.P(
                                    id='info_description',
                                    children='----',
                                    style={'padding': '15px'}
                                )
                            ],
                            className='row flex-display',
                        )
                    ],
                    className="pretty_container four columns",
                )
            ],
            id="third_row",
            className="row flex-display"
        ),
        #----------------------THIRD CONTENT ROW--------------------------------
        html.Div(
            [
                html.Pre(
                    id='click-data',
                    style=styles['pre'],
                ),
            ],
            id='fourth_row',
            className='row flex-display',
        ),
    ]
)
#-----------------------END MAIN CONTENT DIV------------------------------------

def filter_incidents(df,year_slider,applications, incidents):

    dff = df[
        df['appID'].isin(applications)
        & df['Incident'].isin(incidents)
        & (df["Date"] > dt.datetime(year_slider[0],1,1))
        & (df["Date"] < dt.datetime(year_slider[1],1,1))
    ]
    return dff

# def unpack_data(data):
#     flat_data = json.loads(data)
#     flat_data = pd.json_normalize(flat_data)
#     idf = pd.DataFrame(flat_data)
#     idf = idf.rename(columns=
#         {"incident":"Incident",
#          "date.stamp": "Date",
#          "place.location.type": "Type",
#          "place.location.coordinates": "Coordinates",
#          "place.placeName": 'Place',
#          "application.appID": 'appID',
#          "casualties.killed": 'Killed',
#          "casualties.injured": 'Injured',
#         }
#     )
#     idf['Date'] = pd.to_datetime(idf['Date'])
#
#     return idf

# Slider -> count graph
@app.callback(
    [
        Output("year_slider", "value"),
        Output('sMax', 'children'),
        Output('sMin', 'children'),
    ],
    [
        Input("count_graph", "selectedData")
    ]
)
def update_year_slider(count_graph_selected):

    if count_graph_selected is None:
        return [YEAR_RANGE[0], YEAR_RANGE[1]]

    nums = [int(point["pointNumber"]) for point in count_graph_selected["points"]]
    return [ [min(nums) + YEAR_RANGE[0], max(nums) + (YEAR_RANGE[0]+1)], min(nums), max(nums)]

#APPLICATION RADIO ---> DROPDOWN UPDATE
@app.callback(
    Output('application_types', 'value'),
    [
        Input('application_type_selector', 'value')
    ]
)
def application_status(status):
    if status == 'all':
        return list(APPLICATIONS.keys())
    elif status == 'custom':
        return []

# Selectors -> well text
@app.callback(
    [
        Output("iNumber", "children"),
        Output("kNumber", "children"),
        Output("hNumber", "children"),
        Output("yMax", "children"),
        Output('yMin', 'children'),
    ],
    [
        Input('incident_data', 'children'),
        Input("application_types", "value"),
        Input("incident_types", "value"),
        Input("year_slider", "value"),
    ],
)
def update_summary_text(data, application_types, incident_types, year_slider):

    flat_data = json.loads(data)
    flat_data = pd.json_normalize(flat_data)
    idf = pd.DataFrame(flat_data)
    idf = idf.rename(columns=
        {"incident.type":"Incident",
         "incident.killed":"Killed",
         "incident.injured":"Injured",
         "date.stamp": "Date",
         "place.location.type": "Type",
         "place.location.coordinates": "Coordinates",
         "place.placeName": 'Place',
         "application.appID": 'appID',
        }
    )
    idf['Date'] = pd.to_datetime(idf['Date'])

    dff = filter_incidents(idf, year_slider, application_types, incident_types)

    #GETTING TOTALS FOR KILLED
    kSum = dff['Killed'].sum()
    #GETTTING TOTALS FOR INJURIES
    hSum =dff['Injured'].sum()

    return [dff.shape[0], kSum, hSum, year_slider[1],year_slider[0]]

#-------------------MAKE MAP OBJECT--------------------------------------------
@app.callback(
    Output('map_graph', 'figure'),
    [
        Input('incident_data', 'children'),
        Input('application_types', 'value'),
        Input('incident_types', 'value'),
        Input('year_slider', 'value'),
    ],
    [
        State('map_graph', 'relayoutData')
    ],
)
def make_map_graph(data, applications, incidents, years, main_graph_layout):

    flat_data = json.loads(data)
    flat_data = pd.json_normalize(flat_data)
    idf = pd.DataFrame(flat_data)
    idf = idf.rename(columns=
        {"incident.type":"Incident",
         "incident.killed":"Killed",
         "incident.injured":"Injured",
         "date.stamp": "Date",
         "place.location.type": "Type",
         "place.location.coordinates": "Coordinates",
         "place.placeName": 'Place',
         "application.appID": 'appID',
        }
    )
    idf['Date'] = pd.to_datetime(idf['Date'])

    #FILTER INCIDENT DATAFRAME BASED ON USER FILTER CRITERIA
    fidf = filter_incidents(idf, years, applications, incidents)
    #DROP ANY INCIDENT FOR WHICH THERE ARE NO COORDINATES (SUCH AS ON PLANES)
    fidf = fidf.dropna()

    #SPLIT COORDINATES COLUMN OF THE DATAFRAME INTO TWO COLUMNS FOR LATITUDE AND LONGITUDE
    fidf[['Latitude','Longitude']] = pd.DataFrame(fidf.Coordinates.values.tolist(), index=fidf.index)

    tidf = fidf[['_id','Incident','Latitude','Longitude','Place']]

    traces = []
    for incident_class, event in fidf.groupby('Incident'):
        trace = dict(
            type="scattermapbox",
            lon=event["Longitude"],
            lat=event["Latitude"],
            text=event['Place'],
            customdata=event['_id'],
            name=INCIDENTS[incident_class],
            marker=dict(size=8, opacity=0.6),
            )
        traces.append(trace)

    if main_graph_layout is not None:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            main_map_layout["mapbox"]["center"]["lon"] = lon
            main_map_layout["mapbox"]["center"]["lat"] = lat
            main_map_layout["mapbox"]["zoom"] = zoom

    figure = dict(data=traces, layout=main_map_layout)
    return figure
#--------------------MAKE INCIDENT HISTOGRAM-----------------------------------
@app.callback(
    Output("count_graph","figure"),
    [
        Input('incident_data', 'children'),
        Input('year_slider', 'value'),
        Input('application_types', 'value'),
        Input('incident_types', 'value'),
    ]
)
def make_count_graph(data,year_slider,applications, incidents):

    #lDict_count = copy.deepcopy(lDict)
    lDict_count = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), orientation="h"),
        title="Incident Map",
        mapbox=dict(
            #accesstoken=mapbox_access_token,
            style="light",
            center=dict(lon=-78.05, lat=42.54),
            zoom=7,
        ),
    )

    flat_data = json.loads(data)
    flat_data = pd.json_normalize(flat_data)
    idf = pd.DataFrame(flat_data)
    idf = idf.rename(columns=
        {"incident.type":"Incident",
         "incident.killed":"Killed",
         "incident.injured":"Injured",
         "date.stamp": "Date",
         "place.location.type": "Type",
         "place.location.coordinates": "Coordinates",
         "place.placeName": 'Place',
         "application.appID": 'appID',
        }
    )
    idf['Date'] = pd.to_datetime(idf['Date'])

    #FILTER DATAFRAME BASED ON INPUTS
    fidf = filter_incidents(idf, YEAR_RANGE, applications, incidents)

    #CREATE GRAPH SPECIFIC DATAFRAME
    Grdf = fidf[['_id','Date',]]
    Grdf.index = Grdf['Date']
    Grdf = Grdf.resample('A', label='left', closed='right').count()

    #fidf = filter_incidents(idf,[1990,2020])

    colors = []
    for i in range(YEAR_RANGE[0],YEAR_RANGE[1]):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append("rgb(123, 199, 255)")
        else:
            colors.append("rgba(123, 199, 255, 0.2)")

    gData = [
        dict(
            type="scatter",
            mode="markers",
            x=Grdf.index,
            y=Grdf["_id"] / 2,
            name="All Incidents",
            opacity=0,
            hoverinfo="skip",
        ),
        dict(
            type="bar",
            x=Grdf.index,
            y=Grdf["_id"],
            name="All Incidents",
            marker=dict(color=colors),
        ),
    ]

    lDict_count["title"] = "Battery Incidents per Year"
    lDict_count["dragmode"] = "select"
    lDict_count["showlegend"] = False
    lDict_count["autosize"] = True

    figure = dict(data=gData, layout=lDict_count)
    return figure

@app.callback(
    [
        Output('info_date', 'children'),
        Output('info_application', 'children'),
        Output('info_place', 'children'),
        Output('info_description', 'children'),
    ],
    [
        Input('map_graph', 'clickData'),
        Input('incident_data', 'children')
    ]
)
def update_click(clickData, data):

    flat_data = json.loads(data)
    flat_data = pd.json_normalize(flat_data)
    idf = pd.DataFrame(flat_data)
    idf = idf.rename(columns=
        {"incident":"Incident",
         "date.stamp": "Date",
         "place.location.type": "Type",
         "place.location.coordinates": "Coordinates",
         "place.placeName": 'Place',
         "application.appID": 'appID',
         "casualties.killed": 'Killed',
         "casualties.injured": 'Injured',
        }
    )
    idf['Date'] = pd.to_datetime(idf['Date'])

    if clickData is not None:
        step1 = clickData['points']
        step2 = step1[0]
        step3 = step2['customdata']
        chosen = step3
        picked = idf[idf['_id'] == step3]
    else:
        picked = idf



    pDate = picked.iloc[0]['Date']
    pDate = pDate.to_pydatetime()
    pDate = pDate.strftime('%B %d, %Y')

    pApplication = picked.iloc[0]['appID']

    pPlace = picked.iloc[0]['Place']

    pDescription = picked.iloc[0]['description']

    return [pDate, pApplication, pPlace, pDescription]
