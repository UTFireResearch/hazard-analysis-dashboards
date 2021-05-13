import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
import dash_table as dt
import copy
from dash.dependencies import Input, Output, State

from .controls import plot_layout
from app import app

protList=['Unprotected','Protected']

#----------------------APPlICATION LAYOUT---------------------------------------
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
                            'Fire Tools:',
                            style={'margin-bottom': '5px'}
                        ),
                        html.H6(
                            'Steel Heating Under Fire Conditions',
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
                        html.A(
                            html.Button("Fire Research Group",
                                        id="building-deflagration",
                                        style={'width':'100%'}
                            ),
                            href='https://utfireresearch.com',
                            target="_blank",
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
        #---------------START INSTRUCTION FLEX-ROW------------------------------
        html.Div(
            [
                html.Div(
                    [   html.H5(
                            html.B('Instructions'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        html.P(
                            'This tool calculates the lumped transient temperature of steel under fire conditions using standad time-temperature curves. You can select unprotected or protected steel, and various input parameters can be changed.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            'The ISO 834 time-temperature curve is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq1_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'The ASTM E119 time-temperature curve is approximated by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq2_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'The rate of change temperature of the unprotected steel is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq3_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'The rate of change temperature of the protected steel is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq4_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),

                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
        ),
        #----------------MIDDLE INPUTS FLEX ROW--------------------------------
        #----------------START MIDDLE INPUT FLEX ROW---------------------------
        html.Div(
            [
                html.Div(
                    [   html.H5(
                            html.B('Enter Input Parameters'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        #----------SIMULATION TIME FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Simulation Time: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_sim_time',
                                    type='number',
                                    placeholder='hr',
                                    size='15',
                                    value= 3 #-------------REMOVE ME!!!!!!!!
                                ),
                                html.P(
                                    'hours',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Steel Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-----------SECTION FACTOR FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Section Factor: ',
                                    style={'margin-right':'51px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_section_factor',
                                    type='number',
                                    placeholder='1/m',
                                    size='15',
                                    value=200,      #------------REMOVE ME!!!!!!!!!!
                                ),
                                html.P(
                                    '1/m',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #---------------DENSITY FIELD AND LABEL-----------------
                        html.Div(
                            [
                                html.P(
                                    'Density: ',
                                    style={'margin-right':'97px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_density',
                                    type='number',
                                    placeholder='kg/m^3',
                                    size='15',
                                    value=7850,     #----------REMOVE ME!!!!!!!!!!!!
                                ),
                                html.P(
                                    'kg/m^3',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #------------SPECIFIC HEAT FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Specific Heat: ',
                                    style={'margin-right':'60px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_cp',
                                    type='number',
                                    placeholder='J/kg-K',
                                    size='15',
                                    value=600,      #-------REMOVE ME!!!!!!!!!!!!!!!
                                ),
                                html.P(
                                    'J/kg-K',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #--------------EMMISSIVITY FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Emissivity: ',
                                    style={'margin-right':'80px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_emissive',
                                    type='number',
                                    placeholder='',
                                    size='15',
                                    value=0.6,      #---------REMOVE ME!!!!!!!!!!!!!
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Fire Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #--------------FIRE CURVE FIELD AND LABEL---------------
                        html.Div(
                            [
                                html.P(
                                    'Fire Curve: ',
                                    style={'margin-right':'105px', 'margin-top': '5px'}
                                ),
                                html.Div(
                                    dcc.Dropdown(
                                        id='steel_curve',
                                        options=
                                        [
                                            {'label': 'ISO 834', 'value': '834'},
                                            {'label': 'ASTM E119', 'value': 'E119'}
                                        ],
                                        value='834',        #------LEAVE ME HERE!!!!!!!!!
                                    ),
                                    style={'width':'150px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #------HEAT TRANSFER COEFFICIENT FIELD AND LABEL--------
                        html.Div(
                            [
                                html.P(
                                    'Heat Transfer Coefficient: ',
                                    style={'margin-right':'10px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_transfer_coeff',
                                    type='number',
                                    placeholder='W/m^2-K',
                                    size='15',
                                    value=25,       #--------REMOVE ME!!!!!!!!!!!!!!!
                                ),
                                html.P(
                                    'W/m^2-K',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Insulation Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #--------------INSULATION FIELD AND LABEL---------------
                        html.Div(
                            [
                                html.P(
                                    'Steel Protection?: ',
                                    style={'margin-right':'38px', 'margin-top': '5px'}
                                ),
                                html.Div(
                                    dcc.Dropdown(
                                        id='steel_protected',
                                        options=
                                        [
                                            {'label': 'Unprotected', 'value': 'False'},
                                            {'label': 'Protected', 'value': 'True'}
                                        ],
                                        value='False',
                                    ),
                                    style={'width':'150px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.P(
                            'If protected steel, then input the following: ',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        #--------------THICKNESS FIELD AND LABEL----------------
                        html.Div(
                            [
                                html.P(
                                    'Thickness: ',
                                    style={'margin-right':'80px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_thickness',
                                    type='number',
                                    placeholder='m',
                                    size='15',
                                    value=0.050,        #----------REMOVE ME!!!!!!!!
                                ),
                                html.P(
                                    'm',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.Div(
                            [
                                html.P(
                                    'Thermal Conductivity: ',
                                    style={'margin-right':'10px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_conductivity',
                                    type='number',
                                    placeholder='W/m-K',
                                    size='15',
                                    value=0.2,      #-----------REMOVE ME!!!!!!!!!
                                ),
                                html.P(
                                    'W/m-K',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #----------PROTECTED DENSITY FIELD AND LABEL-----------------
                        html.Div(
                            [
                                html.P(
                                    'Density: ',
                                    style={'margin-right':'97px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_protected_density',
                                    type='number',
                                    placeholder='kg/m^3',
                                    size='15',
                                    value=150,      #---------REMOVE ME!!!!!!!!!
                                ),
                                html.P(
                                    'kg/m^3',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #------PROTECTED SPECIFIC HEAT FIELD AND LABEL----------
                        html.Div(
                            [
                                html.P(
                                    'Specific Heat: ',
                                    style={'margin-right':'60px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='steel_protected_cp',
                                    type='number',
                                    placeholder='J/kg-K',
                                    size='15',
                                    value=1200,     #---------REMOVE ME!!!!!!!!!!
                                ),
                                html.P(
                                    'J/kg-K',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Calculate Transient Steel Temperature >>',
                                    id='submit_steel',
                                    style={
                                    "margin-left": '2px',
                                    "margin-bottom": '15px',
                                    "margin-top": '15px'
                                    }
                                )
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
        ),
        #------------------------RESULTS ROW------------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='steel_graph'),
                                    ],
                                    className='column'
                                ),
                                html.Div(
                                    [
                                        dt.DataTable(
                                            id='steel_table',
                                            style_table={'height': '300px', 'overflowY': 'auto'},
                                            page_action='none',
                                        ),
                                    ],
                                    className='column'
                                ),
                            ],
                            className='row flex-display',
                        ),

                        html.P(id='cMessage'),
                    ],
                    className='pretty_container twelve columns',
                ),
            ],
            className='row flex-display',
        ),
        #----------------BOTTOM ACKNOWLEDGEMENTS ROW----------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'This calculator was develop by Dr. Kris Overholt and it is based on a Matlab script by Randall McDermott. This calculator is powered by the free and open source tools Python, Numpy, Matplotlib, and Plotly|Dash.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className= "row flex-display",

        ),
        #------------ROW FOR HIDDEN DIVS HOLDING EXECUTION PARAMETERS-----------
        html.Div(id='steel_comp_state',style={'display':'none'}),
    ]
), #---------------------END LAYOUT--------------------------------------------


@app.callback(
    [
        Output('cMessage','children'),
        Output('steel_graph','figure'),
        Output('steel_comp_state','children'),
        Output('steel_table','columns'),
        Output('steel_table','data'),
    ],
    [
        Input('submit_steel','n_clicks'),
    ],
    [
        State('steel_sim_time','value'),
        State('steel_section_factor','value'),
        State('steel_density','value'),
        State('steel_cp','value'),
        State('steel_emissive','value'),
        State('steel_curve','value'),
        State('steel_transfer_coeff','value'),
        State('steel_protected','value'),
        State('steel_thickness','value'),
        State('steel_conductivity','value'),
        State('steel_protected_density','value'),
        State('steel_protected_cp','value'),
    ]
)
def steel_btn_execute(btn, time, section, dense, cp, emissive, curve, transfer, protected, thickness,pConduct, pDense, pCP):

    #-------------INITIALIZE COMPLETION STATE AND ERROR MESSAGE-----------------
    steel_complete = True
    steel_eMessage = ''

    #-----------STAGE SETTING CODE FOR PLOT GENERATION--------------
    steel_data=[]
    steel_layout = copy.deepcopy(plot_layout)

    figure = dict(data=steel_data, layout=steel_layout)

    #---------------------CREATE INPUT PARAMETER LIST---------------------------
    inList = [time, section, dense, cp, emissive, curve, transfer, protected, thickness, pDense, pCP]

    #-------------------INPUT CHECKING------------------------------------------
    if time >= 1000:
        steel_eMessage = 'Simulation time must be less than 1,000 hours'
        return steel_emessage, figure, 'FALSE'

    #-----------------------CALCULATIONS----------------------------------------
    dt = 1/120 # hours
    sigma = 0.0000000567 # W/m^2-K^4

    t = np.arange(0,time+dt,dt)

    t_half = t+dt/2

    T_steel = np.zeros(len(t)+1)
    dT_steel = np.zeros(len(t))
    T_steel[0] = 20

    T_steel_protected = np.zeros(len(t)+1)
    dT_steel_protected = np.zeros(len(t))
    T_steel_protected[0] = 20

    if curve == '834':
          T_fire_half = 20 + 345 * np.log10(8*(t_half*60)+1)

    if curve == 'E119':
        T_0 = 20
        T_fire_half = 750 * (1-np.exp(-3.79553*np.sqrt(t_half))) + 170.41*(np.sqrt(t_half)) + T_0

    for i in range(0,len(t)):
        dT_steel[i] = section * 1/(dense * cp) * (transfer*(T_fire_half[i] - T_steel[i]) + emissive*sigma*((T_fire_half[i]+273)**4 - (T_steel[i]+273)**4)) * (dt*3600)
        T_steel[i+1] = T_steel[i] + dT_steel[i]

    if protected == 'True':
        for i in range(0,len(t)):
            dT_steel_protected[i] = section * (pConduct/(thickness*dense*cp)) * (dense*cp / (dense*cp + (section*thickness*pDense*pCP) / 2)) * (T_fire_half[i] - T_steel_protected[i]) * (dt*3600)
            T_steel_protected[i+1] = T_steel_protected[i] + dT_steel_protected[i]

    #----------------PLOTTING CODE----------------------------------------------
    steel_layout["title"] = "Steel Temperature vs. Time"
    steel_layout["showlegend"] = False
    steel_layout["xaxis"] = {"title": {"text": "Time (hr)"}}
    steel_layout["yaxis"] = {"title": {"text": "Temperature (C)"}}
    # steel_layout['shapes'] = dict(
    #                             type='line',
    #                             x0 = 0,
    #                             y0 = 600,
    #                             x1 = max(t),
    #                             y1 = 600,
    #                             line=dict(
    #                                 color="Black",
    #                                 width=4,
    #                                 dash="dashdot",
    #                             )
    #                         )

    if protected == 'False':
        steel_data = [
            dict(
                type="scatter",
                mode="lines",
                x=t,
                y=T_steel[:-1],
                name="Unprotected",
                opacity=1,
                hoverinfo="skip",
            ),
        ]

    if protected == 'True':
        steel_data = [
            dict(
                type="scatter",
                mode="lines",
                x=t,
                y=T_steel[:-1],
                name="Unprotected",
                opacity=1,
                hoverinfo="skip",
            ),
            dict(
                type="scatter",
                mode="lines",
                x=t,
                y=T_steel_protected[:-1],
                name="Protected",
                opacity=1,
                hoverinfo="skip",
            ),
        ]

    figure = dict(data=steel_data, layout=steel_layout)

    return '', figure, 'TRUE',
