import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output,dash_table,State

dash.register_page(__name__, path='/')

genres = ['Action',
 'Adventure',
 'Animation',
 "Children's",
 'Comedy',
 'Crime',
 'Documentary',
 'Drama',
 'Fantasy',
 'Film-Noir',
 'Horror',
 'Musical',
 'Mystery',
 'Romance',
 'Sci-Fi',
 'Thriller',
 'War',
 'Western']



layout = html.Div(
    [
            dbc.Row([

                dbc.Col([
                    html.P("Select Genre:",
                        style={"textDecoration": "underline"}),
                    dcc.Dropdown(id='genre_list', multi=False, value='Comedy',
                                options=[
                                {"label":k,"value":k} for k in genres
                                ],
                                )
                ],# width={'size':5, 'offset':1, 'order':1},
                ),

                dbc.Col([
                    html.P("Select Method:",
                        style={"textDecoration": "underline"}),
                    dcc.Dropdown(id='method_list', multi=False, value="Rating",
                                options=["Rating","Popularity"],
                                )
                ], #width={'size':5, 'offset':0, 'order':2},
                ),
                

            ]),

            dbc.Button("Submit",id='Submit0'),

            
            dbc.Row([
                html.H2('Movies you may like based on genre',style={'text-align':'center'}),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                
                                dbc.CardImg(
                                    id="card01_1",
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
                                
                                dbc.CardImg(
                                    id="card02_1",
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
                                
                                dbc.CardImg(
                                    id="card03_1",
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
                                
                                dbc.CardImg(
                                    id="card04_1",
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
                                
                                dbc.CardImg(
                                    id="card05_1",
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
                                
                                dbc.CardImg(
                                    id="card06_1",
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
                                
                                dbc.CardImg(
                                    id="card07_1",
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
                                
                                dbc.CardImg(
                                    id="card08_1",
                                    bottom=True
                                ),
                            ],
                            style={"width": "18rem"},
                        )
                    ]
                )
            
        ])
        
    
    ]
)

