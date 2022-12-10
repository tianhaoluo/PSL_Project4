import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output,dash_table,State

dash.register_page(__name__)

image_prefix = "https://liangfgithub.github.io/MovieImages/"
def toURL(mid):
    return image_prefix+mid+".jpg"



layout = html.Div(
    [
        dbc.Row([
                html.H2('Rate as many movies as possible (at least 3 for personalized results)',style={'text-align':'center'}),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card01_2i",
                                    src=toURL("1"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating1", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                ),
                 dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card02_2i",
                                    src=toURL("2"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating2", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card03_2i",
                                    src=toURL("3"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating3", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card04_2i",
                                    src=toURL("4"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating4", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                )
            
        ]),

        dbc.Row([
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card05_2i",
                                    src=toURL("5"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating5", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                ),
                 dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card06_2i",
                                    src=toURL("6"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating6", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card07_2i",
                                    src=toURL("7"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating7", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card08_2i",
                                    src=toURL("8"),
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                        dcc.Dropdown(id="rating8", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                        )
                    ]
                )
            
        ]),
        html.Br(),
        dbc.Button("Submit",id='Submit1',size='lg'),
        dbc.Button("Reset Movies to rate",id='Reset',size='lg',style={"margin-left": "15px"}),
        dbc.Row([
                html.H2('Your recommendations (wait for 10s: free tier of server)',style={'text-align':'center'}),
                html.H2('',id="warn",style={'text-align':'center'}),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank1',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card01_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                ),
                 dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank2',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card02_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank3',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card03_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank4',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card04_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                )
            
        ]),

        dbc.Row([
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank5',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card05_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                ),
                 dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank6',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card06_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank7',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card07_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H3('Rank8',style={'text-align':'center'}),
                                dbc.CardImg(
                                    id="card08_2o",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                )
            
        ]),
        
    ]
)
