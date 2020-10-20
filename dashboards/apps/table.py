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
                            href="https://www.utfireresearch.com",
                            target='_blank ',
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

        #---------------------FIRST CONTENT ROW--------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Lithium-ion batteries are already a common feature of society, powering billions of electronic devices. Growth in renewable energy and electric vehicles in the future is only likely to increase the number of these batteries. By 2030, global production of lithium-ion batteries is expected to reach nearly 2 TWh. Consequently, the risks posed by lithium-ion battery failures will only grow and it is essential that they are sufficiently understood.',
                                        html.Br(),
                                        html.Br(),
                                        'These tools are intended to help policy-makers and researches better understand lithium-ion fire and explosion hazards.'
                                        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Viverra nibh cras pulvinar mattis nunc sed. Adipiscing at in tellus integer feugiat scelerisque varius morbi. Viverra tellus in hac habitasse platea. Ut sem nulla pharetra diam sit amet. Nunc sed blandit libero volutpat sed cras ornare arcu. Diam phasellus vestibulum lorem sed risus ultricies tristique. Aliquam sem et tortor consequat id porta nibh venenatis cras.'
                                    ]
                                )
                            ],
                            style={'margin-right': '25px', 'margin-left': '25px'}
                        ),
                    ],
                    className="pretty_container seven columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            ['Global Battery Production', html.Br(),'(2020)'],
                                            style={'textAlign':'left'}
                                        ),
                                    ],
                                    className='two-thirds column',
                                    style={'margin-left':'20px'}
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            '350 GWh',
                                            style={'line-height': '40px', 'textAlign': 'center','margin-left': '35px'},
                                        ),
                                    ],
                                    className='one-third column',
                                    style={'display':'flex','align-items':'center'},
                                ),
                            ],
                            className='row flex-display',
                        ),
                        html.Hr(style={'margin-top':'10px','margin-bottom':'10px'}),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            [
                                                'Battery and Energy Storage',
                                                html.Br(),
                                                'Market (2019)'
                                            ],
                                            style={'textAlign':'left'}
                                        )
                                    ],
                                    className='two-thirds column',
                                    style={'margin-left': '20px'}
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            '$44.2 Billion',
                                            style={'line-height': '40px', 'textAlign': 'center','margin-left': '35px'},
                                        ),
                                    ],
                                    className='one-third column',
                                    style={'display':'flex','align-items':'center'},
                                )
                            ],
                            className='row flex-display'
                        ),
                    ],
                    className="pretty_container five columns",
                ),
            ],
            id="intro-row",
            className="row flex-display",
        ),
        #-------------------SECOND CONTENT ROW---------------------------------
        html.Div(
            [   #-----------------SECOND ROW PRETTY CONTAINER------------------
                html.Div(
                    [   #--------------SECOND ROW CONTENT COLUMN----------------
                        html.Div(
                            [   #------------CONTENT TITLE----------------------
                                html.Div(
                                    [
                                        html.H6(children='Vent Gas Flammability Data')
                                    ],
                                    className="row flex-display"
                                ),
                                #-------------CONTENT PARAGRAPH-----------------
                                html.Div(
                                    [
                                        html.P(children='When lithium-ion batteries fail, they produce large volumes of flammable and toxic gases. The composition of these gases depends on a variety of factors including battery chemistry, form factor, and state-of-charge (SOC). This tool curates available data from academic literature characterizing the composition of battery vent gases and provides estimated flammability parameters for these mixtures.'
                                        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                        ),
                                    ],
                                    className='row flex-display',
                                ),
                                #-------------LINK BUTTON-----------------------
                                html.A(
                                    html.Button("Go To Tool",
                                                id="building-deflagration",
                                                style={'width':'100%','margin-top': '20px'}
                                    ),
                                    href='/apps/hazard_analysis',
                                ),
                            ],
                            className='two-thirds column',
                            style={'margin-left': '25px'}
                        ),
                        #--------------SECOND ROW IMAGE COLUMN-----------------
                        html.Div(
                            [
                                html.Img(
                                    src=('/assets/composition-plot.PNG'),
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
                            [   #---------CONTENT TITLE------------------------
                                html.Div(
                                    [
                                        html.H6(children='Fire and Explosion Incidents')
                                    ],
                                    className="row flex-display"
                                ),
                                #---------DESCRIPTION CONTENT-------------------
                                html.Div(
                                    [
                                        html.P(children='Batteries are ubiquitous in modern society and range in scale from mega-watt energy storage systems to the single cells in mobile phones. The damage that results when these systems fail covers a similar scale. This tool provides access to a curated database of battery failure incidents at all scales and around the globe. While the number of jurisdictions involved makes it difficult to build a truly comprehensive dataset, the aim is to allow researchers to understand the scope of battery safety issues and identify failure patterns.'
                                        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                        )
                                    ]
                                ),
                                #----------LINK BUTTON--------------------------
                                html.A(
                                    html.Button("Comign Soon",
                                                id="building-deflagration",
                                                style={'width':'100%', 'margin-top':'20px'}
                                    ),
                                    #href='/apps/incide',
                                ),
                            ],
                            className='two-thirds column',
                            style={'margin-left': '25px'}
                        ),
                        #-----------------THIRD ROW IMAGE COLUMN---------------
                        html.Div(
                            [
                                html.Img(
                                    src=('/assets/incident-map.PNG'),
                                    style={
                                        'height': '200px',
                                    }
                                ),
                            ],
                            className='one-third column',
                            style={'textAlign': 'center'}
                        ),
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
                            [   #--------------CONTENT TITLE--------------------
                                html.Div(
                                    [
                                        html.H6(children='Deflagration Vent Calculator')
                                    ],
                                    className="row flex-display"
                                ),
                                #---------------CONTENT PARAGRAPH---------------
                                html.Div(
                                    [
                                        html.P(children='A common mitigation strategy for legacy fire and explosion hazards is the use of blow-off vents to prevent injury and structural damage by relieving pressure. This tool uses our battery vent gas dataset in conjunction with the process described in NFPA 68 to provide a first-order estimate of the deflagration vent area needed to protect a structure against a given explosion event involving battery vent gas.'
                                        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                        )
                                    ]
                                ),
                                #--------------TOOL LINK BUTTON-----------------
                                html.A(
                                        html.Button("Go To Tool",
                                                    id="building-deflagration",
                                                    style={'width':'100%', 'margin-top':'20px'}
                                        ),
                                        href='/apps/vent_calculator'
                                ),
                            ],
                            className='two-thirds column',
                            style={'margin-left': '25px'}
                        ),
                        #-----------------FOURTH ROW IMAGE COLUMN---------------
                        html.Div(
                            [
                                html.Img(
                                    src=('/assets/Vent_Size.png'),
                                    style={
                                        'height': '200px',
                                    }
                                ),
                            ],
                            className='one-third column',
                            style={'textAlign': 'center'}
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
        #-------------------FIFTH CONTENT ROW-----------------------------------
        html.Div(
            [   #------------------FIFTH ROW PRETTY CONTAINER-------------------
                html.Div(
                    [   #-----------------FIFTH ROW CONTENT COLUMN--------------
                        html.Div(
                            [   #---------CONTENT TITLE------------------------
                                html.Div(
                                    [
                                        html.H6(children='Explosion Calculator')
                                    ],
                                    className="row flex-display"
                                ),
                                #---------DESCRIPTION CONTENT-------------------
                                html.Div(
                                    [
                                        html.P(children='When lithium-ion batteries fail, they produce large volumes of flammable and toxic gases. The composition of these gases depends on a variety of factors including battery chemistry, form factor, and state-of-charge (SOC). This tool uses our dataset of battery vent gas to estimate the time vs. pressure history of a explosion due to burning battery vent gas.'
                                        #'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
                                        )
                                    ]
                                ),
                                #----------LINK BUTTON--------------------------
                                html.A(
                                    html.Button("Go To Tool",
                                                id="building-deflagration",
                                                style={'width':'100%', 'margin-top':'20px'}
                                    ),
                                    href='/apps/explosion_calculator',
                                ),
                            ],
                            className='two-thirds column',
                            style={'margin-left': '25px'}
                        ),
                        #-----------------FIFTH ROW IMAGE COLUMN---------------
                        html.Div(
                            [
                                html.Img(
                                    src=('/assets/firework.png'),
                                    style={
                                        'height': '200px',
                                    }
                                ),
                            ],
                            className='one-third column',
                            style={'textAlign': 'center'}
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
    ]
) #--------------------------END MAIN PAGE CONTAINER---------------------------
