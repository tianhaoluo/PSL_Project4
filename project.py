import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,dash_table,State  # pip install dash (version 2.0.0 or higher)
import dash
import dash_bootstrap_components as dbc
import collections
from dash_extensions import Lottie
import pickle
import numpy as np
from surprise import Dataset, NormalPredictor, Reader,KNNWithMeans
from surprise.model_selection import cross_validate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server

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

topMovies = {'m1240': 'Terminator, The (1984)',
 'm1374': 'Star Trek: The Wrath of Khan (1982)',
 'm480': 'Jurassic Park (1993)',
 'm1265': 'Groundhog Day (1993)',
 'm32': 'Twelve Monkeys (1995)',
 'm2997': 'Being John Malkovich (1999)',
 'm1387': 'Jaws (1975)',
 'm1200': 'Aliens (1986)',
 'm780': 'Independence Day (ID4) (1996)',
 'm1291': 'Indiana Jones and the Last Crusade (1989)',
 'm1': 'Toy Story (1995)',
 'm2858': 'American Beauty (1999)',
 'm1036': 'Die Hard (1988)',
 'm1610': 'Hunt for Red October, The (1990)',
 'm1580': 'Men in Black (1997)',
 'm2791': 'Airplane! (1980)',
 'm1221': 'Godfather: Part II, The (1974)',
 'm34': 'Babe (1995)',
 'm1214': 'Alien (1979)',
 'm1704': 'Good Will Hunting (1997)',
 'm2028': 'Saving Private Ryan (1998)',
 'm50': 'Usual Suspects, The (1995)',
 'm2762': 'Sixth Sense, The (1999)',
 'm590': 'Dances with Wolves (1990)',
 'm1968': 'Breakfast Club, The (1985)',
 'm2683': 'Austin Powers: The Spy Who Shagged Me (1999)',
 'm592': 'Batman (1989)',
 'm1127': 'Abyss, The (1989)',
 'm858': 'Godfather, The (1972)',
 'm1270': 'Back to the Future (1985)',
 'm3471': 'Close Encounters of the Third Kind (1977)',
 'm1210': 'Star Wars: Episode VI - Return of the Jedi (1983)',
 'm296': 'Pulp Fiction (1994)',
 'm1197': 'Princess Bride, The (1987)',
 'm2571': 'Matrix, The (1999)',
 'm2916': 'Total Recall (1990)',
 'm2000': 'Lethal Weapon (1987)',
 'm1307': 'When Harry Met Sally... (1989)',
 'm1394': 'Raising Arizona (1987)',
 'm648': 'Mission: Impossible (1996)',
 'm318': 'Shawshank Redemption, The (1994)',
 'm1097': 'E.T. the Extra-Terrestrial (1982)',
 'm377': 'Speed (1994)',
 'm1213': 'GoodFellas (1990)',
 'm541': 'Blade Runner (1982)',
 'm2959': 'Fight Club (1999)',
 'm924': '2001: A Space Odyssey (1968)',
 'm1196': 'Star Wars: Episode V - The Empire Strikes Back (1980)',
 'm2797': 'Big (1988)',
 'm912': 'Casablanca (1942)',
 'm3175': 'Galaxy Quest (1999)',
 'm2628': 'Star Wars: Episode I - The Phantom Menace (1999)',
 'm2396': 'Shakespeare in Love (1998)',
 'm1198': 'Raiders of the Lost Ark (1981)',
 'm457': 'Fugitive, The (1993)',
 'm110': 'Braveheart (1995)',
 'm2355': "Bug's Life, A (1998)",
 'm1617': 'L.A. Confidential (1997)',
 'm2918': "Ferris Bueller's Day Off (1986)",
 'm1721': 'Titanic (1997)',
 'm2599': 'Election (1999)',
 'm2987': 'Who Framed Roger Rabbit? (1988)',
 'm1259': 'Stand by Me (1986)',
 'm919': 'Wizard of Oz, The (1939)',
 'm1193': "One Flew Over the Cuckoo's Nest (1975)",
 'm3114': 'Toy Story 2 (1999)',
 'm589': 'Terminator 2: Judgment Day (1991)',
 'm3578': 'Gladiator (2000)',
 'm608': 'Fargo (1996)',
 'm260': 'Star Wars: Episode IV - A New Hope (1977)',
 'm356': 'Forrest Gump (1994)',
 'm527': "Schindler's List (1993)",
 'm593': 'Silence of the Lambs, The (1991)',
 'm1136': 'Monty Python and the Holy Grail (1974)',
 'm2716': 'Ghostbusters (1984)',
 'm2174': 'Beetlejuice (1988)',
 'm2291': 'Edward Scissorhands (1990)',
 'm3793': 'X-Men (2000)'}



def system1(genre,method,data):
    genres = list(data.index.unique())
    if genre not in genres:
        print('Genre must be one of the following')
        print(" ".join(genres))
        return
    if method not in ['Rating','Popularity']:
        print('Method must be either "Rating" or "Popularity"')
        return
    #First method for recommendation (Rating): for movies with more than 100 ratings, get top 10 by average rating
    if method == 'Rating':
        df = data[data['numRatings'] > 100].loc[genre].sort_values('Rating',ascending=False)[:10]
    #Second method for recommendation (Popularity): for recent movies (year > 1998), get top 10 by number of ratings received
    else:
        #For smaller categories like 'Western', 'Film-Noir' etc., we need to relax the definition of 'recent'
        lookback = 6 if genre == 'Western' else 4 if genre in ('Musical','Fantasy','War','Mystery') else 10 if genre == 'Film-Noir' else 2
        #The film need to be 'recent' enough and have a lot of ratings (sort by descending, I don't care whether the rating is good or bad for this method)
        recent_year = max(data.loc[genre]['year'])-lookback
        df = data[data['year'] > recent_year].loc[genre].sort_values('numRatings',ascending=False)[:10]
    df = df[['MovieID','Title','numRatings','Rating']].merge(movies0[["MovieID","Genres"]],on='MovieID',how='left')
    return df

def display_movie_to_rate(movie_id1,movie_id2,i,j):
    return dbc.Row([
            dbc.Col(
                [
                    html.P(topMovies[movie_id1],style={"textDecoration": "underline"}),
                    dcc.Dropdown(id='movie'+str(i)+"_rating", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                                )
                ]
            ),
            dbc.Col(
                [
                    html.P(topMovies[movie_id2],style={"textDecoration": "underline"}),
                    dcc.Dropdown(id='movie'+str(j)+"_rating", multi=False, value=None,
                                options=[
                                {"label":k,"value":k} for k in [1,2,3,4,5]
                                ],
                                )
                ]
            )
        ])

def generate_random_movies():
    ids = np.random.choice([k for k in topMovies],12,replace=False)
    res = []
    hm = {}
    for i in range(0,12,2):
        res.append([ids[i],ids[i+1],i,i+1])
        hm[i] = ids[i]
        hm[i+1] = ids[i+1]
    return res,hm

random_movies, id2movieid = generate_random_movies()

ratings = pd.read_table("https://liangfgithub.github.io/MovieData/ratings.dat",sep="::",header=None,engine='python')
ratings.columns = ['UserID','MovieID','Rating','Timestamp']
ratings['UserID'] = ratings['UserID'].apply(lambda x:'u'+str(x))
ratings['MovieID'] = ratings['MovieID'].apply(lambda x:'m'+str(x))
movies_id = list(ratings['MovieID'].unique())
reader = Reader(rating_scale=(1, 5))
train_df = ratings.rename(columns={"UserID":"userID","MovieID":"itemID","Rating":"rating"}).drop(columns=['Timestamp'])


movies = pd.read_table("https://liangfgithub.github.io/MovieData/movies.dat",sep="::",header=None,engine='python',encoding='latin-1')
#movies0 = movies.copy()
movies.columns = ['MovieID','Title','Genres']
#movies0 = movies.copy()
movies['year'] = movies['Title'].apply(lambda x:int(x[-5:-1]))
movies['MovieID'] = movies['MovieID'].apply(lambda x:'m'+str(x))
movies0 = movies.copy()
movies['Genres'] = movies['Genres'].apply(lambda x:x.split("|"))
movies_w_ratings = movies.explode('Genres').merge(ratings,on='MovieID',how='left')

try:
    with open("sys1_result.pickle",'rb') as f:
        sys1_result = pickle.load(f)
except:
    
    sys1_data = movies_w_ratings.groupby(['Genres','MovieID','Title']).agg({'UserID':'count','Rating':np.mean,'year':'first'}).rename(columns={'UserID':'numRatings'}).reset_index().set_index('Genres')

    genres = movies_w_ratings['Genres'].unique()
    sys1_result = {}
    for genre in sys1_data.index.unique():
        for method in ['Rating','Popularity']:
            sys1_result[genre,method] = system1(genre,method,sys1_data)
    with open('sys1_result.pickle', 'wb') as handle:
        pickle.dump(sys1_result, handle)


# ------------------------------------------------------------------------------
# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [dbc.Row(
                    dbc.Col(html.H1(id="title",children="RecSys by genre",
                                    className='text-center text-primary mb-4'),
                            )
                ),
    

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

            dbc.Row(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2('Recommendations',style={'text-align':'center'}),
                            dash_table.DataTable(id='rectable1')
                        ])
                    ]),
                ],  #width={'size':5, 'offset':1},
                #xs=8, sm=8, md=8, lg=5, xl=5
                )
            )
        
    ],xs=12, sm=12, md=12, lg=7, xl=7),
    dbc.Col(id='part2',
        children=[dbc.Row(
                    dbc.Col([html.H1(id="title2",children="RecSys by IBCF",
                                    className='text-center text-primary mb-4'),
#                             html.H3(children="Refresh to get a new set of movies to rate",
#                                     className='text-center text-primary mb-4')]
                            ]
                            )
                ),
                dbc.Row([dbc.Col(id="movies_to_rate",children=[display_movie_to_rate(movie_id1,movie_id2,i,j) for movie_id1,movie_id2,i,j in random_movies])]),
                dbc.Button("Submit",id='Submit'),
                dbc.Row(
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H2('ICBF Recommendations',style={'text-align':'center'}),
                                html.H3(id="warning",style={'text-align':'center'}),
                                dash_table.DataTable(id='rectable2')
                            ])
                        ]),
                    ],  #width={'size':5, 'offset':1},
                    #xs=8, sm=8, md=8, lg=5, xl=5
                    )
                )
        ]
    ,xs=12, sm=12, md=12, lg=5, xl=5)

    ], className="g-0", justify='start'),  # Horizontal:start,center,end,between,around


  

    


    

],fluid=True)

@app.callback(
    [
    Output(component_id="rectable1",component_property='data'),
    Output(component_id="rectable1",component_property='columns')
    ],
    [
    Input(component_id="Submit0",component_property="n_clicks")
    ],
    [State(component_id="genre_list",component_property='value'),
    State(component_id='method_list',component_property='value')
    ],
    prevent_initial_call=True,
    )
def recsys1(_,genre,method):
    df = sys1_result[genre,method].reset_index().copy()
    print(df.head())
    df['Rating'] = df["Rating"].apply(lambda x:round(x,2))
    df.rename(columns={'numRatings':"#ratings","Rating":"AvgRating"},inplace=True)
    data = df.to_dict(orient='records')
    columns = [{'name': col, 'id': col} for col in ['Title','Genres',"#ratings"]] if method == "Popularity" else [{'name': col, 'id': col} for col in ['Title','Genres',"AvgRating"]]
    return data,columns

@app.callback(
    [
    Output(component_id="warning",component_property='children'),
    Output(component_id="rectable2",component_property='data'),
    Output(component_id="rectable2",component_property='columns')
    ],
    [Input(component_id="Submit",component_property='n_clicks')
    ],
    [State(component_id="movie"+str(i)+"_rating",component_property='value' ) for i in range(12)],
    prevent_initial_call=True,
    )
def submit_button(n_clicks,r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11):
    print("Submitted")
    ratings = [r0,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11]
    user_rating = {}
    for i in range(12):
        print(f"i={i}")
        curid = 'movie'+str(i)+"_rating"
        movieid = id2movieid[i]
        r = ratings[i]
        print(curid,movieid,r)
        if r is not None:
            user_rating[movieid] = int(r)
    if len(user_rating) < 3:
        print("Rate at least 3 movies")
        return "Rate at least 3 movies to get prediction!",None,None
    ms = []
    rs = []
    for m,r in user_rating.items():
        ms.append(m)
        rs.append(r)
    n_r = len(user_rating)


    test_df = pd.DataFrame({"userID":["new"]*n_r,"itemID":ms,"rating":rs})

    random_users = np.random.choice(train_df['userID'].unique(),400,replace=False)
    train_df_sampled = train_df[train_df['userID'].isin(random_users)].copy()

    data_train = Dataset.load_from_df(pd.concat([train_df_sampled,test_df]), reader).build_full_trainset()
    algo = KNNWithMeans(sims_options={"user_based":False,"name":"cosine"})
    algo.fit(data_train)

    res = {}
    for movie in movies_id:
        if movie in user_rating:
            continue
        cur = algo.predict('new',movie)
        res[movie] = cur[3]
    rec_list = [x[1] for x in sorted([(r,m) for m,r in res.items()])[-10:][::-1]]
    out_df = movies0[movies0['MovieID'].isin(rec_list)]
    data = out_df.to_dict(orient='records')
    columns = [{'name': col, 'id': col} for col in ['Title','Genres']]
    return "",data,columns

    
    

if __name__ == '__main__':
    app.run_server(debug=True)
