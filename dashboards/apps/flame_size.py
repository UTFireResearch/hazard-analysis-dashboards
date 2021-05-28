import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import dash_table as dt
import dash_table
import copy

from app import app
from dash.dependencies import Input, Output, State
from .controls import plot_layout

columntest=[{'name': 'Height (m)', 'id': 'Height (m)'},
            {'name': 'Heskestad Temp.', 'id': 'Heskestad Temp.'},
            {'name': 'McCaffrey Temp.', 'id': 'McCaffrey Temp.'}]

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
                            'Flame Height and Plume Centerline Temperature Calculator',
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
                            'This tool calculates the flame height and plume centerline temperatures based on the correlations by Heskestad and McCaffrey.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.H6(
                            'Governing Equations',
                            style={'margin-left':'20px'}
                        ),
                        html.P(
                            'The flame height correlation by Heskestad is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq1_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'The plume centerline temperature correlation by Heskestad is given by:',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq2_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'which is valid above the flame height.',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            'The plume centerline temperature correlation by McCaffrey is given by:',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq3_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'which is valid above the flame height. The McCaffrey plume temperature correlation can be used in the intermittent and continuous flaming regions with other constants. For the sake of simplicity, only the plume region form of the correlation is used here.',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            [
                            'Note: An ambient temperature (T',
                            html.Sub('\u221E'),
                            ') of 20',
                            html.Sup('\u00B0'),
                            'C is used.'
                            ],
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            [
                            'More information on the above equations can be found in the textbook',
                            html.I('Enclosure Fire Dynamics by Karlsson and Quintiere.')
                            ],
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.H6(
                            'Characteristic Fire Size',
                            style={'margin-left':'20px'}
                        ),
                        html.P(
                            'Additionally, the characteristic fire size (or nondimensional heat release rate) is a useful quantity to relate the energy output of a fire to its physical diameter. Q* is calculated by:',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq4_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            [
                            'The properties of air at standard temperature and pressure are used as \u03C1',
                            html.Sub('\u221E'),
                            ' = 1.204 kg/m',
                            html.Sup('3'),
                            ', c',
                            html.Sub('p'),
                            ' = 1.005 kJ/kg-K,',
                            ' T',
                            html.Sub('\u221E'),
                            ' = 293 K, and g = 9.81 m/s',
                            html.Sup('2'),
                            '. More details can be found in NUREG 1824.',
                            ],
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),

                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
        ),
        #----------------START MIDDLE INPUT FLEX ROW---------------------------
        html.Div(
            [
                html.Div(
                    [   html.H5(
                            html.B('Input Parameters'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        html.H6(
                            'Fire Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-------MAXIMUM FIRE SIZE FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Fire Size: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='flame_size_in',
                                    type='number',
                                    placeholder='kW',
                                    size='15',
                                    value=400,  #DELETE ME!!!! -- (PROBABABLY)
                                ),
                                html.P(
                                    'kW',
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
                        #------------FIRE DIAMETER FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Fire Diameter: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='flame_diameter_in',
                                    type='number',
                                    placeholder='m',
                                    size='15',
                                    value=1,    #DELETE ME!!!!!! -- (PROBABLY)
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
                        #-------MAXIMUM FIRE SIZE FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Radiative Fraction: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                    id='flame_rad_frac',
                                    type='number',
                                    placeholder='',
                                    size='15',
                                    value=0.3   #DELETE ME!!!!! -- (PROBABLY)
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
                        #------------CALCULATE BUTTON--------------------------
                        html.Div(
                            [
                                html.Button(
                                    'Calculate Plume Characteristics >>',
                                    id='flame_calc_button',
                                    style={
                                    "margin-left": '2px',
                                    "margin-bottom": '15px',
                                    "margin-top": '15px'
                                    },
                                    n_clicks=0,
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

                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id='flame_eMessage_p',
                        ),
                    ],
                    className='pretty_container twelve columns',
                ),
            ],
            className='row flex-display',
            id='flame_eMessage_row'
        ),
        #-------------------RESULTS ROW-----------------------------------------
        html.Div(
            [
                #---------------RESULTS PRETTY CONTAINER------------------------
                html.Div(
                    [
                        html.H5(
                            html.B('Results:'),
                            style={
                            "margin-bottom": "15px",
                            "color": "maroon"
                            }
                        ),
                        #----------------FLEX ROW INSIDE RESULTS CONTAINER------
                        html.Div(
                            [
                                #---------TEXT RESULTS DIV----------------------
                                html.Div(
                                    [
                                        html.H6(
                                            'Non-Dimensional HRR:',
                                            style={'margin-left':'15px'}
                                        ),
                                        html.P(
                                            'The characteristic fire size (Q*) is',
                                            style={'display':'inline-block', 'color':'black', 'padding-right':'5px', 'margin-left':'25px'},
                                        ),
                                        html.P(
                                            html.B(id='flame_char_size'),
                                            style={'display':'inline-block'},
                                        ),
                                        html.H6(
                                            'Heskestad Flame Height:',
                                            style={'margin-left':'15px'},
                                        ),
                                        html.P(
                                            html.B(id='flame_message1'),
                                            style={'margin-left':'25px'},
                                        ),
                                        html.P(
                                            html.B(id='flame_message2'),
                                            style={'margin-left':'25px'},
                                        ),
                                    ],
                                    #style={'float':'left','display':'flex'},
                                ),
                                # html.H6(
                                #     'Heskestad and McCaffrey Plume Centerline Temperatures:',
                                #     style={'margin-left':'15px', 'margin-top':'20px'}
                                # ),
                                #--------------GRAPH SUB CONTAINER--------------
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='centerline_graph',
                                            style={'margin-left':'20px', 'height':550, 'width':750}
                                        ),
                                    ],
                                    style={'margin-left':'10px'}
                                ),
                                #-------------DATA TABLE SUB CONTAINER----------
                                html.Div(
                                    [
                                        dt.DataTable(
                                            id='flame_table',
                                            columns = columntest,
                                            data = [],
                                            #fixed_rows={'headers': True},
                                            style_cell_conditional=[
                                                {'if': {'column_id': 'Height (m)'},
                                                 'width': '30%'},
                                                {'if': {'column_id': 'Heskestad Temp. (\u00B0C)'},
                                                 'width': '35%'},
                                                {'if': {'column_id': 'McCaffrey Temp. (\u00B0C)'},
                                                 'width': '35%'}

                                            ],
                                            style_table={'height': '550px', 'minWidth':'500px', 'overflowY': 'auto'}
                                        ),
                                    ],
                                    style={'margin-left':'15px'},
                                ),
                            ],
                            className='row flex-display'
                        ),
                    ],
                    className='pretty_container twelve columns',
                ),
                # html.Div(
                #     [
                #         html.H5(
                #             html.B('Values:'),
                #             style={
                #             "margin-bottom": "15px",
                #             "color": "maroon"
                #             }
                #         ),
                #     ],
                #     className='pretty_container four columns'
                # )
            ],
            className='row flex-display',
            style={'display':'none'},
            id='flame_results_row',
        ),
        # html.Div(
        #     [
        #         html.Div(
        #             [
        #                 html.Div(
        #                     [
        #                         dt.DataTable(
        #                             id='flame_table',
        #                             columns = columntest,
        #                             data = [],
        #                             style_table={'height': '600px', 'overflowY': 'auto'}
        #                         ),
        #                     ],
        #                     style={'width':'400px'},
        #                 ),
        #             ],
        #             className='pretty_container twelve columns'
        #         )
        #     ],
        #     className='row flex-display',
        # ),
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
        html.Div(
            [
                html.Div(id='flame_comp_state',children='FALSE',style={"display": "none"}),
            ],
            style={'display':'none'},
        ),
    ],
), #---------------------END LAYOUT--------------------------------------------
def flame_in_check(finlist):

    if finlist[0] <= 0 or finlist[1] <= 0 or finlist[2] <= 0:
        eMessage = 'Please ensure that all values are greater than zero'
        return [False, eMessage]
    else:
        return [True, '']

@app.callback(
        [
            Output('flame_results_row', 'style'),
            Output('flame_eMessage_row','style'),
        ],
        [
            Input('flame_comp_state', 'children'),
        ],
        [
            State('flame_calc_button','n_clicks'),
        ]
)
def visibility_toggle(state,btn):

    show = {'display':'block'}
    hide = {'display':'none'}

    if state == 'TRUE' and btn > 0:
        return show, hide
    elif state != 'TRUE' and btn > 0:
        return hide, show
    else:
        return hide, hide


@app.callback(
    [
        Output('flame_comp_state','children'),
        Output('flame_eMessage_p','children'),
        Output('flame_char_size','children'),
        Output('flame_message1','children'),
        Output('flame_message2','children'),
        Output('centerline_graph','figure'),
        Output('flame_table','data'),
        Output('flame_table','columns'),
    ],
    [
        Input('flame_calc_button','n_clicks'),
    ],
    [
        State('flame_size_in','value'),
        State('flame_diameter_in','value'),
        State('flame_rad_frac','value'),
    ]
)
def flame_calc_execute(btn, size, diameter, radFrac):

    columnd = [
        'Height (m)',
        'Heskestad Temp. (\u00B0C)',
        'McCaffrey Temp. (\u00B0C)'
    ]

    flame_complete1 = 'TRUE'
    flame_complete2 = 'FALSE'
    flame_eMessage = ''

    flame_data = []
    flame_layout = copy.deepcopy(plot_layout)

    flame_figure = dict(data=flame_data, layout=flame_layout)

    inList = [size, diameter, radFrac]

    inCheck = flame_in_check(inList)

    if btn > 0 and inCheck[0]:

        D = diameter # m
        Q = size # kW
        X_r = radFrac

        #  =================================
        #  = Plume temperature calculation =
        #  =================================

        Q_c = (1-X_r) * Q
        z_0 = 0.083 * Q**(2/5) -1.02 * D
        L = -1.02 * D + 0.235*(Q**(2/5))
        above_flame = 5*L

        z = np.arange(L+L*0.3,L+above_flame,(L+above_flame)/50)
        delta_T_0_hes = np.zeros(len(z))
        delta_T_0_mcc = np.zeros(len(z))

        for height in range(0,len(z)):
            delta_T_0_hes[height] = 25 * (Q_c**(2/5)/(z[height]-z_0))**(5/3) + 20

        for height in range(0,len(z)):
            delta_T_0_mcc[height] = 22.3 * (Q**(2/5)/(z[height]))**(5/3) + 20

        #  ======================
        #  = Q_star calculation =
        #  ======================

        # Density (kg/m3)
        rho = 1.204

        # Specific heat (kJ/kg-K)
        c_p = 1.005

        # Ambient temperature (K)
        T_inf = 293

        # Gravitational acceleration
        g = 9.81

        Q_star = Q / (rho * c_p * T_inf * np.sqrt(g*D) * D**2)

        height = L
        cHeight = L*3.28

        message1 = f'For a {size:.2f} kW fire with a diameter of {diameter:.2f} m'
        message2 = f'The flame height is {height:.2f} m ({cHeight:.2f} ft)'

        max1 = max(delta_T_0_hes)
        max2 = max(delta_T_0_mcc)
        max3 = max(max1, max2)
        xLine = L

        #===============================================
        # ==========PLOTTING CODE=======================
        #===============================================
        flame_layout['title'] = 'Hakestad and McCaffrey Plume Centerline Temperatures:'
        flame_layout['showlegend'] = True
        flame_layout["xaxis"] = {"title": {"text": "Height (m)"}}
        flame_layout["yaxis"] = {"title": {"text": "Plume Centerline Temperature (\u00B0C)"}}
        flame_layout["xaxis"]['range'] = [0, L+above_flame]
        flame_layout['shapes'] = [
            {
                'type':'line',
                'x0': xLine,
                'y0': 0,
                'x1':xLine,
                'y1': max3,
                'line': {
                    'color':'black',
                    'width':2,
                    'dash':'dashdot'
                    }
            }
        ]

        flame_data = [
            dict(
                type="scatter",
                mode="lines",
                x=z,
                y=delta_T_0_hes,
                name="Hekestad",
                opacity=1,
                hoverinfo="skip",
            ),
            dict(
                type="scatter",
                mode="lines",
                x=z,
                y=delta_T_0_mcc,
                name="McCaffrey",
                opacity=1,
                hoverinfo="skip",
            ),
        ]

        flame_figure = dict(data=flame_data, layout=flame_layout)

        dhes = [round(i) for i in delta_T_0_hes]
        dmcc = [round(k) for k in delta_T_0_mcc]
        zr = [round(j,3) for j in z]

        # dhes = []
        # for i in range(len(delta_T_0_hes)):
        #
        #     dhes[i] = round(delta_T_0_hes[i],2)
        #
        # dmcc = []
        # for i in range(len(delta_T_0_mcc)):
        #
        #     dmcc[i] = round(delta_T_0_mcc[i],2)

        df = pd.DataFrame(list(zip(zr,dhes,dmcc)), columns=columnd)

        dtable = df.to_dict('rows')
        ctable = [{'name': i, 'id': i} for i in df.columns]

        return flame_complete1, inCheck[1], str(round(Q_star,3)), message1, message2, flame_figure, dtable, ctable

    else:
        return 'FALSE', inCheck[1], '', '', '', flame_figure, [], []
