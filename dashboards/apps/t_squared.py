import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import copy
import json
import pandas as pd

from dash_extensions import Download
from dash.dependencies import Input, Output, State
from .controls import plot_layout
from app import app
from dash_extensions.snippets import send_data_frame, send_file

import uuid
import os
import flask

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
                            'Fire Ramp Calculator',
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

            ],
            className='row flex-display',
        ), #----------------------END INSTRUCTIONS FLEX-ROW--------------------
        #---------------START INPUT PARAMETER FLEX ROW-------------------------
        html.Div(
            [
                #-----------------START INPUT PRETTY CONTAINER------------------
                html.Div(
                    [
                        html.H5(
                            html.B('Select Input Parameters'),
                            style={
                            "margin-bottom": "15px",
                            "color": "maroon"
                            }
                        ),
                        #----------------START FIRE COEFFICIENT SECTION--------
                        html.H6(
                            'Fire Growth Coefficient',
                            style={
                            "margin-bottom": "5px",
                            "margin-left": "20px"
                            }
                        ),
                        dcc.RadioItems(
                            options=[
                                {'label': 'Slow: 0.00293 kW/s^2', 'value': 'slow'},
                                {'label': 'Medium: 0.01172 kW/s^2', 'value': 'medium'},
                                {'label': 'Fast: 0.0469 kW/s^2', 'value': 'fast'},
                                {'label': 'Ultrafast: 0.1876 kW/s^2', 'value': 'ultrafast'},
                                {'label': 'Other:', 'value': 'custom'},
                            ],
                            value='slow',
                            id='fire_growth_coefficient',
                            labelStyle={
                            'display': 'inline-block',
                            "margin-left": "20px",
                            "margin-bottom": "20px"
                            }
                        ),
                        dcc.Input(
                            id='custom_alpha',
                            type='number',
                            placeholder='Custom: kW/S\u00b2',
                            style={"margin-left": "20px"},
                        ),
                         # ------------- END FIRE COEFFICIENT SECTION --------

                        #------------START FIRE PARAMETERS SECTION -------------
                        html.H6(
                            'Fire Parameters',
                            style={
                            "margin-bottom": "5px",
                            "margin-left": "20px"
                            }
                        ),
                        html.P(
                            'Select when the t-squared fire ramp should stop:',
                            style={
                            "margin-left": "20px"
                            }
                        ),
                        dcc.RadioItems(
                            options=[
                                {'label': 'Maximum HRR:________ kW', 'value': 'max_HRR'},
                                {'label': 'Maximum Time:_______ S', 'value': 'max_time'},
                            ],
                            value='max_HRR',
                            id='stop_ramp_sel',
                            labelStyle={
                            'display': 'inline-block',
                            "margin-left": "20px",
                            "margin-bottom": "20px"
                            }
                        ),
                        dcc.Input(
                            id='stop_ramp_choice',
                            type='number',
                            style={"margin-left": "20px"},
                        ),
                         #----------------END FIRE PARAMETERS SECTION --------

                        #-----------------START OUTPUT PARAMETERS SECTION-------
                        html.H6(
                            'Additional Output Parameters (optional)',
                            style={
                            "margin-bottom": "5px",
                            "margin-left": "20px"
                            }
                        ),
                        html.P(
                            'Select additional outputs:',
                            style={
                            "margin-left": "20px"
                            }
                        ),
                        dcc.Checklist(
                            id='t_squared_output_opt',
                            options=[
                                {'label': 'Downloadable CSV file', 'value': 'CSV'},
                                {'label': 'FDS HRR Ramp Text', 'value': 'FDS'},
                            ],
                            value=[],
                            labelStyle={
                            'display': 'inline-block',
                            "margin-left": "20px",
                            "margin-bottom": "20px"
                            }
                        ),
                        html.Div(
                            [
                                html.P(
                                'FDS HRR Vent Size:  ',
                                style={
                                    "margin-right": "5px",
                                    "margin-bottom": "0px",
                                    "margin-top": "0px"}
                                ),
                                #----------VENT SIZE INPUT ROW------------------
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='FDS_1',
                                        type='number',
                                        placeholder='meters',
                                        ),

                                        html.P(
                                            ' X ',
                                            style={
                                                "margin-right": "5px",
                                                "margin-left": "5px"
                                            }
                                        ),

                                        dcc.Input(
                                        id='FDS_2',
                                        type='number',
                                        placeholder='meters',
                                        ),
                                    ],
                                    className="row",
                                    style={"margin-bottom": "20px"}
                                ),
                            ],
                            style={"margin-left": "20px"},
                            #className="row",
                        ),
                        html.Button(
                            'Calculate t-Squared Fire Ramp',
                            id='t_squared_submit',
                            style={
                                "margin-left": "20px",
                            },
                            n_clicks = 0,
                        ), #

                    ],
                    className='pretty_container five columns'
                ), # ------ END INPUT PRETTY CONTAINER-------------------------

                html.Div(
                    [   html.H5(
                            html.B('Instructions'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        # dcc.Markdown(
                        #     '''
                        #     '''
                        # ),
                        html.Div(
                            [
                                html.P(
                                    [
                                    'This tool calculates a t-squared (time squared or t',
                                    html.Sup('2'),
                                    ') heat release rate (HRR) curve, which is commonly used to estimate transient fire growth for fire protection design purposes. The t-squared parabolic growth equation is given by:',
                                    ],
                                    style={"margin": "10px", "font-size": "20"}
                                ),
                                # html.P(
                                #     '[Q_dot = alpha*t^2]',
                                #     style={"margin": "10px"}
                                # ),
                                html.Img(
                                    src=('/assets/t2_eq1_mod.PNG'),
                                    style={'height': '40px', 'margin-left': '20px'},
                                ),
                                html.P(
                                    'where [Q] is the HRR (kW), [\u03B1] is the fire growth coefficient (kW/s^2), and t is time (s).',
                                    style={"margin": "10px", 'margin-bottom':'25px'}
                                ),
                                html.P(
                                    'Some commonly used fire growth coefficients are provided, or a custom coefficient can be specified. The t-squared fire ramp can be configured to grow until a specified HRR or time is attained. The output is aplot of the HRR vs. Time.',
                                    style={"margin": "10px", 'margin-bottom':'25px'}
                                ),
                                html.P(
                                    'Additionally, a spreadsheet of the results (CSV file) and Fire Dynamics Simulator (FDS) syntax (TXT file) can also be output and saved.',
                                    style={"margin": "10px"}
                                ),
                            ],
                            style={"font-size": "20px"}
                        ),

                    ],
                    className='pretty_container eight columns'
                ),
            ],
            className='row flex-display',
        ),
        #----------------OUTPUT DISPLAY FLEX ROW-------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.H5(
                            html.B('Results:'),
                            style={
                            "margin-bottom": "15px",
                            "color": "maroon"
                            }
                        ),
                        dcc.Graph(id='t2_ramp_graph',),
                    ],
                    id='t2_result_container',
                    className='pretty_container nine columns',
                ),
                html.Div(
                    [
                        html.H5(
                            html.B('Output Files:'),
                            style={
                            "margin-bottom": "15px",
                            "color": "maroon"
                            }
                        ),
                        html.P(
                            'If you selected additional output options, buttons to download the selected files will appear below:',
                            style={'margin':'15px'},
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Download CSV File",
                                    id='d_btn_csv',
                                    style={'margin':'15px'},
                                ),
                                Download(id="t2_download_csv")
                            ],
                            id="csv_btn",
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Download FDS File",
                                    id='d_btn_fds',
                                    style={'margin':'15px'},
                                ),
                                Download(id="t2_download_fds")

                                #---------FILE DOWLOAD LINK TEST BUTTON
                                # html.A(
                                #     html.Button("Download Test File",
                                #                 id="fds_test_btn",
                                #                 style={'width':'100%'}
                                #     ),
                                #     href='/dashboards/stage/test.txt',
                                #     target="_blank",
                                #     style={"float": "right", "width": "240px"}
                                # ),

                            ],
                            id="fds_btn",
                        ),
                        #html.P('--------',id='error_message'),
                    ],
                    id='t2_file_container',
                    className='pretty_container four columns',
                ),
            ],
            id='t2_results_row',
            className='row flex-display',
        ),
        #----------------BOTTOM ACKNOWLEDGEMENTS ROW---------------------------
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
        html.Div(id='comp_state',style={'display':'none'}),
        html.Div(id='comp_state1', style={'display':'none'}),
        html.Div(id='comp_btn1', style={'display':'none'}),
        html.Div(id='comp_btn2', style={'display':'none'}),
        html.Div(id='time_holder', style={'display':'none'}),
        html.Div(id='HRR_holder', style={'display':'none'}),
        html.Div(id='job_ID', style={'display':'none'}),
        html.Div(id='ramp_area', style={'display':'none'}),
    ]
)

#-------------NON-CALLBACK FUNCTION DEFINITIONS

#--------------CALL BACKS SECTION----------------------------------------------
@app.callback(
    [
        Output('stop_ramp_choice','placeholder'),
        Output('stop_ramp_choice','value'),
    ],
    [
        Input('stop_ramp_sel','value'),
    ],
)
def fire_stop_label(choice):

    if choice == 'max_HRR':

        return "kW", None

    if choice == 'max_time':

        return 'seconds', None

@app.callback(
    [
    Output('t2_ramp_graph','figure'),
    Output('comp_state', 'children'),
    Output('time_holder', 'children'),
    Output('HRR_holder', 'children'),
    Output('job_ID','children'),
    Output('ramp_area','children'),
    ],
    [
    Input('t_squared_submit','n_clicks'),
    ],
    [
    State('fire_growth_coefficient','value'),
    State('custom_alpha', 'value'),
    State('FDS_1', 'value'),
    State('FDS_2', 'value'),
    State('stop_ramp_sel','value'),
    State('stop_ramp_choice','value'),
    State('t_squared_output_opt','value'),
    State('fire_growth_coefficient','value'),
    ],
)
def primary_t_squared(b_click,alpha_select,cAlpha,FDS1,FDS2,stop_choice,stop_value,output_opt,growth):

    completion_state = 'TRUE'
    eMessage = ''
    # #----------------CHECKING ALPHA VALUE INPUTS--------------------------------
    #
    # #----------------CHECKING RAMP STOP VALUE INPUT-----------------------------
    # if not stop_value:
    #     t2_message = 'Error -- Please enter a stopping criteria\n'
    #     completion_state = 'FALSE'
    #     #return type(stop_choice).__name__
    #
    # #-------------------CHECKING OUTPUT VENT SIZE INPUTS------------------------
    # if ('FDS' in output_opt) and not FDS1 and not FDS2:
    #     t2_message = 'Error -- Please provide values for both HRR vent size dimensions in the Output section.'
    #     completion_state = 'FALSE'
    #
    #-----------PARSING INPUTS AND CONVERTING TO NUMERICS----------------------
    if b_click!=0 and stop_choice == 'max_HRR':
        try:
            max_HRR = float(stop_value)
        except:
            #t2_message = 'Please input a valid maximum HRR value.'
            completion_state = 'FALSE'

    if b_click!=0 and stop_choice == 'max_time':
        try:
            max_time = float(stop_value)
        except:
            #t2_message = 'Please input a valid maximum time value.'
            completion_state = 'FALSE'

    if b_click!=0 and growth == 'custom':
        try:
            growth_co = float(cAlpha)
        except:
            #t2_message = 'Plase input a valid growth coefficient.'
            completion_state = 'FALSE'

    #------------SET MAXIMUM VALUE FOR END PARAMETER (IF SELECTED)--------------
    try:
        if stop_value > 99999.0:
            stop_value_M = 99999.0
        else:
            stop_value_M = stop_value

            stop_value_M = stop_value
    except:
        completion_state = 'FALSE'

    ttest = type(stop_value).__name__
    #-----------SET ALPHA VALUE BASED ON SELECTION------------------------------
    try:
        if alpha_select == 'slow':
            gAlpha=0.00293
            title_alpha = "(slow growth)"
        if alpha_select == 'medium':
            gAlpha=0.01172
            title_alpha = "(medium growth)"
        if alpha_select == 'fast':
            gAlpha=0.0469
            title_alpha = "(fast growth)"
        if alpha_select == 'ultrafast':
            gAlpha=0.1876
            title_alpha = "(ultrafast growth)"
        if alpha_select == 'custom':
            gAlpha = cAlpha
            title_alpha = r"($\alpha$ = %0.4f kW/s$^2$)" % gAlpha
    except:
        completion_state = 'FALSE'
    #---------------------------------------------------------------------------

    #------------------CALCULATE T-SQUARED RAMP---------------------------------
    try:
        if stop_choice == 'max_HRR':
            max_time = np.ceil(np.sqrt(stop_value_M/gAlpha))
            t2_time = np.arange(max_time + 1)
            t2_HRR = gAlpha * t2_time**2

            t2_message = 'Results:\n' + str(int(stop_value_M)) + 'kW is attained at a time of ' + str(int(max_time)) + ' seconds'

            t2_HRR_o = np.ndarray.tolist(t2_HRR)
            t2_HRR_o = json.dumps(t2_HRR_o)
            t2_time_o = np.ndarray.tolist(t2_time)
            t2_time_o = json.dumps(t2_time_o)

        if stop_choice == 'max_time':
            max_time = stop_value_M
            t2_time = np.arange(stop_value_M + 1)
            t2_HRR = gAlpha * t2_time**2
            t2_m_time = np.max(t2_time)
            t2_m_HRR = gAlpha* max_time**2

            t2_message = 'Results:\n' + str(int(t2_m_HRR)) + 'kW is attained at a time of ' + str(int(t2_m_time)) + ' seconds'

            t2_HRR_o = np.ndarray.tolist(t2_HRR)
            t2_HRR_o = json.dumps(t2_HRR_o)
            t2_time_o = np.ndarray.tolist(t2_time)
            t2_time_o = json.dumps(t2_time_o)
    except:
        completion_state = 'FALSE'

        t2_HRR_o = None
        t2_time_o = None

    #-----------------SAVE .CSV FILE FOR USER DOWNLOAD--------------------------

    # try:
    #     if 'CSV' in output_opt:
    #
    #         header_rows = np.array([['alpha', gAlpha], ['Time (s)', 'HRR (kW)']])
    #         output_data = np.column_stack([time, hrr])
    #         csv_output = np.row_stack([header_rows, output_data])
    #         csv_output = csv_output.tolist()
    #
    #         csv_filename = './t_squared/case%i.csv' % jobid
    #
    #         for n in range(len(csv_output)):
    #             outstring = csv_output[n] + ['\n']
    #             stats(csv_filename, ','.join(outstring))
    # except:
    #     completion_state = 'FALSE'

    #----------------SAVE .FDS TEXT FOR FDS HRR RAMP----------------------------
    # try:
    #     if 'FDS' in output_opt:
    #
    #         time_list = np.arange(0, np.max(time) + 1, 10)
    #         time_list = time_list.tolist()
    #         fds_filename = './t_squared/fds%i.txt' % jobid
    #         surf_string = "&SURF ID='fire', RAMP_Q='tsquared', HRRPUA=%0.1f, COLOR='RED' /" % (np.max(hrr) / fds_fire_ramp_area)
    #         stats(fds_filename, surf_string + '\n')
    #
    #         for n in time_list:
    #             fds_f_value = hrr[t2_time == n] / np.max(hrr)
    #             ramp_text = "&RAMP ID='tsquared', T=%0.1f, F=%0.2f /" % (n, fds_f_value)
    #             outstring = ramp_text + '\n'
    #             stats(fds_filename, outstring)
    # except:
    #     completion_state = 'FALSE'

    #----------------PLOTTING CODE----------------------------------------------
    data=[]
    layout = copy.deepcopy(plot_layout)

    try:
        data = [
            dict(
                type="scatter",
                mode="lines",
                x=t2_time,
                y=t2_HRR,
                name="t-Squared Ramp Graph",
                opacity=1,
                hoverinfo="skip",
            )
        ]

        layout["title"] = "t-Squared Ramp" + title_alpha
        layout["showlegend"] = False
        layout["xaxis"] = {"title": {"text": "time (s)"}}
        layout["yaxis"] = {"title": {"text": "Heat Release Rate (HRR)"}}

        figure = dict(data=data, layout=layout)

    except:
        completion_state = 'FALSE'
        figure = dict(data=data, layout=layout)

    #type(stop_value).__name__
    jobid = np.random.randint(10000000)

    if FDS1 and FDS2:
        FDS_ramp = FDS1*FDS2
    else:
        FDS_ramp = None

    return figure, completion_state,t2_time_o,t2_HRR_o,jobid,str(FDS_ramp)

#-------THIS CALLBACK DETERMINES WHICH OF THE RESULTS SECTION ELEMENTS ARE
#-------VISIBLE BASED ON THE PROVIDED INFORMATION
#-------------------------------------------------------------------------
@app.callback(
        [
        Output('t2_results_row', 'style'),
        #Output('t2_file_container', 'style'),
        Output('csv_btn', 'style'),
        Output('fds_btn', 'style'),
        ],
        [
            Input('t_squared_submit', 'n_clicks'),
            Input('comp_state', 'children'),
            Input('ramp_area','children')
        ],
        [
            State('t_squared_output_opt','value'),
        ]
)
def visibility_toggle(first_click,compp,rampA,out_opt):

    display_style = {
        "margin-bottom": "15px",
        "color": "maroon"
        }

    hidden_style = {
        "margin-bottom": "15px",
        "color": "maroon",
        "display": "none"
        }

    btn_hidden = {'display':'none'}

    btn_shown = {'display':'block'}

    #---DISPLAY STATE OF THE FDS BUTTON
    if ('FDS' in out_opt) and rampA != 'None':
        FDS_display = btn_shown
    else:
        FDS_display = btn_hidden

    #---DISPLAY STATE OF THE CSV BUTTON
    if ('CSV' in out_opt):
        CSV_display = btn_shown
    else:
        CSV_display = btn_hidden

    #--DISPLAY STATE OF THE RESULTS CONTAINER
    if first_click > 0 and compp == 'TRUE':
        t2_row_state = display_style
    else:
        t2_row_state = hidden_style

    # if first_click > 0 and compp == 'TRUE':
    #
    #     #---SUCCESSFUL COMPLETION, FDS AND CSV SELECTED, RAMP AREA ENTERED
    #     if ('FDS' in out_opt) and ('CSV' in out_opt):
    #         return display_style,display_style,btn_shown,btn_shown
    #
    #     # #---SUCCESSFUL COMPLETION, FDS AND CSV SELECTED, NO RAMP AREA ENTERED
    #     # elif ('FDS' in out_opt and rampA == 'None') and ('CSV' in out_opt):
    #     #     return display_style,display_style,btn_shown,btn_hidden
    #     #
    #     #---SUCCESSFUL COMPLETION, FDS ONLY SELECTED, RAMP AREA ENTERED
    #     elif ('FDS' in out_opt) and ('CSV' not in out_opt):
    #         return display_style,display_style,btn_hidden,btn_shown
    #
    #     # #---SUCCESSFUL COMPLETION, FDS ONLY SELECTED, NO RAMP AREA ENTERED
    #     # elif ('FDS' in out_opt and rampA == 'None') and ('CSV' not in out_opt):
    #     #     return display_style,display_style,btn_hidden,btn_hidden
    #
    #     elif ('FDS' not in out_opt) and ('CSV' in out_opt):
    #         return display_style,display_style,btn_shown,btn_hidden
    #
    #     elif ('FDS' not in out_opt) and ('CSV' not in out_opt):
    #         return display_style,display_style,btn_hidden,btn_hidden
    #
    #     else:
    #         return display_style,display_style,btn_shown,btn_shown
    # else:
    #     return hidden_style,hidden_style,btn_shown,btn_shown

    return t2_row_state,CSV_display,FDS_display

@app.callback(
    Output('t2_download_csv','data'),
    [
        Input('d_btn_csv','n_clicks'),
    ],
    [
        State('time_holder','children'),
        State('HRR_holder','children'),
        State('job_ID','children'),
    ]
)
def csv_download(cb_clicks,time,HRR,jobidd):

    #---------UNPACK JSON DATA
    flat_time = json.loads(time)
    flat_HRR = json.loads(HRR)
    #---------CREATE PANDAS DATAFRAME
    int_dict = {'Time (s)': flat_time,'HRR (kW/s^2)': flat_HRR}

    t2_df = pd.DataFrame(int_dict)

    csv_title = 't_squard - ' + str(jobidd) + '.csv'

    return send_data_frame(t2_df.to_csv, filename=csv_title)


@app.callback(
    Output('t2_download_fds', 'data'),
    [
        Input('d_btn_fds','n_clicks'),
    ],
    [
        State('time_holder','children'),
        State('HRR_holder','children'),
        State('job_ID','children'),
        State('ramp_area','children'),
    ]
)
def fds_download(cb_clicks,time,HRR,jobidd,rArea):

    if time and HRR and jobidd and rArea:
        #---------UNPACK JSON DATA
        flat_time = json.loads(time)
        flat_HRR = json.loads(HRR)

        flat_time = np.asarray(flat_time)
        flat_HRR = np.asarray(flat_HRR)

        rArea = float(rArea)
        #-----------------------------
        time_list = np.arange(0, np.max(flat_time) + 1,10)
        time_list = time_list.tolist()

        #---------CREATE FILENAME
        fds_filename='FDS Ramp - ' + str(jobidd) + '.txt'
        # fds_path = f"stage/{fds_filename}"

        #----------GENERATING ACTUAL FDS FILE TEXT
        surf_string = "&SURF ID='fire', RAMP_Q='tsquared', HRRPUA=%0.1f, COLOR='RED' /" % (np.max(flat_HRR) / rArea)

        #---------OPENING AND WRITING THE FILE
        # with open(fds_path, 'w') as fds_file:
        #     fds_file.write(fds_text)
        # stats(fds_filename, surf_string + '\n')
        fds_out_string = surf_string + '\n'
        f_value_list = []

        for n in time_list:
            fds_f_value = flat_HRR[flat_time == n] / np.max(flat_HRR)
            ramp_text = "&RAMP ID='tsquared', T= %0.1f, F=%0.4f /" % (n, fds_f_value)
            fds_out_string = fds_out_string + ramp_text + '\n'
            # stats(fds_filename, outstring)
            f_value_list.append(fds_f_value)

    else:
        fds_filename = 'error.txt'
        fds_out_string = 'error'

    et_message = str(f_value_list)

    # except:
    #     flat_time = [0,0,0]
    #     flat_HRR = [0,0,0]
    #     rArea = 1
    #
    #     fds_filename='FDS Ramp - ' + 'error' + '.txt'
    #     fds_out_string = 'error'

    # uri =fds_path

    return dict(content=fds_out_string, filename=fds_filename)

# @app.server.route("/stage/<path:path>")
# def serve_static(fds_path):
#     root_dir = os.getcwd()
#     return flask.send_from_directory(os.path.join(root_dir, "stage"), filename=path)

# @app.callback(
#     Output('t2_download_fds','data'),
#     [
#     Input('d_btn_fds','n_clicks')
#     ]
# )
# def fds_btn_click(clicks):
#     return dict(content="Hello world!", filename="hello.txt")
#     # return send_file('/stage/test.txt')

# @app.server.route("/apps/fds")
# def download_test():
#     return dict(content="Hello world!", filename="hello.txt")
#     # return send_file('/dashboards/stage/test.txt',
#     #                  # mimetype = 'text/csv',
#     #                  # attachment_filename='test.txt',
#     #                  # as_attachment=True
#     #                  )
