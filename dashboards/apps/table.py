
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
                            }
                        )
                    ],
                    id="logo",
                    className='one-third column',
                ),
                #---------------------CENTER HEADER COLUMN---------------------
                html.Div(
                    [   #-------------------HEADER TITLE-----------------------
                        html.H3(
                            'Battery Vent Gas Hazard Analysis',
                        ),
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "30px"}
                ),
                #--------------------LEGACY NAVIGATION BUTTONS-----------------
                #---------------------RIGHT HEADER COLUMN----------------------
                html.Div(
                    [
                    #     html.A(
                    #         html.Button("Building Deflagration",
                    #                     id="building-deflagration",
                    #                     style={'width': '100%'}
                    #         ),
                    #         href="/apps/explosion_calculator",
                    #         style={"float": "right", 'width': '250px'}
                    #     ),
                    #     html.A(
                    #         html.Button("Vent Sizing",
                    #                     id="vent-sizing",
                    #                     style={'width': '100%'}
                    #         ),
                    #         href="/apps/vent_calculator",
                    #         style={"float": "right","width": '250px'}
                    #     )
                        html.A(
                            html.Button("Learn More",
                                        id="building-deflagration",
                                        style={'width':'100%'}
                        ),
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className='row flex-display',
            style={
                "magin-bottom": "25px"
            }
        ), #-----------------------END HEADER DIV------------------------------
        html.Div(
            [

            ]
        ),
    ]
) #--------------------------END MAIN PAGE CONTAINER---------------------------
