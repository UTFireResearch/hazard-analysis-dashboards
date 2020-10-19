import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#--------------------------MAIN PAGE CONTAINER---------------------------------
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
                            'Battery Fire and Explosion Hazards:',
                            style={'margin-bottom': '5px'}
                        ),
                        html.H6(
                            'Analysis Tools',
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
                            html.Button("Learn More",
                                        id="building-deflagration",
                                        style={'width':'100%'}
                            ),
                            href="/apps/table",
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
                "magin-bottom": "30px"
            }
        ), #-----------------------END HEADER DIV------------------------------

        #---------------------FIRST CONTENT ROW--------------------------------
        html.Div(
            [
                html.Div(
                    [

                    ],
                    className="pretty_container eight columns"
                ),
                html.Div(
                    [

                    ],
                    className="pretty_container four columns",
                ),
            ],
            id="intro-row",
            className="row flex-display",
        ),
        #-------------------SECOND CONTENT ROW---------------------------------
        html.Div(
            [   #-----------------SECOND ROW PRETTY CONTAINER------------------
                html.Div(
                    [   #--------------SECOND ROW CONTENT COLUMN---------------
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(children='Vent Gas Flammability Data')
                                    ],
                                    className="row"
                                ),
                                html.Div(
                                    [
                                        html.P(children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
                                    ]
                                ),
                            ],
                            className='two-thirds column',
                        ),
                        #--------------SECOND ROW IMAGE COLUMN-----------------
                        html.Div(
                            [
                                html.Img(
                                    src=('/assets/composition-plot.png'),
                                    style={
                                        'height': '200px',
                                    }
                                )
                            ],
                            style={'textAlign': 'center'},
                            className='one-third column',
                        )
                    ],
                    className="pretty_container twelve columns"
                ),
            ],
            className="row flex-display",
        ),
        #--------------------THIRD CONTENT ROW----------------------------------
        html.Div(
            [   #------------------THIRD ROW PRETTY CONTAINER-------------------
                html.Div(
                    [   #-----------------THIRD ROW CONTENT COLUMN--------------
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(children='Fire and Explosion Incidents')
                                    ],
                                    className="row"
                                ),
                                html.Div(
                                    [
                                        html.P(children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
                                    ]
                                ),
                            ],
                            className='two-thirds column'
                        ),
                        #-----------------THIRD ROW IMAGE COLUMN---------------
                        html.Div(
                            [
                                #content to be added
                            ]
                        )
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
        #--------------------FOURTH CONTENT ROW---------------------------------
        html.Div(
            [   #------------------FOURTH ROW PRETTY CONTAINER------------------
                html.Div(
                    [   #---------------FOURTH ROW CONTENT COLUMN---------------
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(children='Deflagration Vent Calculator')
                                    ],
                                    className="row"
                                ),
                                html.Div(
                                    [
                                        html.P(children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
                                    ]
                                ),
                            ],
                            className='two-thirds column',
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
    ]
) #--------------------------END MAIN PAGE CONTAINER---------------------------
