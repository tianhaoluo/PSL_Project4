from dash import Dash, dcc, html, Input, Output,dash_table,State  # pip install dash (version 2.0.0 or higher)
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pickle
from surprise import Dataset, NormalPredictor, Reader,KNNWithMeans
from surprise.model_selection import cross_validate
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                ,use_pages = True)

server = app.server

with open("sys1_result.pickle",'rb') as f:
    sys1_result = pickle.load(f)

with open("movies_w_ratings.pickle",'rb') as f:
    movies_w_ratings = pickle.load(f)

ratings = pd.read_table("https://liangfgithub.github.io/MovieData/ratings.dat",sep="::",header=None,engine='python')
ratings.columns = ['UserID','MovieID','Rating','Timestamp']
ratings['UserID'] = ratings['UserID'].apply(lambda x:'u'+str(x))
ratings['MovieID'] = ratings['MovieID'].apply(lambda x:'m'+str(x))
movies_id = list(ratings['MovieID'].unique())
reader = Reader(rating_scale=(1, 5))
train_df = ratings.rename(columns={"UserID":"userID","MovieID":"itemID","Rating":"rating"}).drop(columns=['Timestamp'])

random_users = np.random.choice(train_df['userID'].unique(),500,replace=False)
train_df_sampled = train_df[train_df['userID'].isin(random_users)].copy()
random_users = None
ratings = None
train_df = None

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

image_prefix = "https://liangfgithub.github.io/MovieImages/"

recsys_names = {"Pg1":"Genre-based","Pg2":"IBCF-based"}

print([page['name'] for page in dash.page_registry.values()])

app.layout = dbc.Container(
    [
        # main app framework
        html.Div("Recommender System App with Dash", style={'fontSize':50, 'textAlign':'center'}),
        html.Div([
            dcc.Link(recsys_names[page['name']]+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ],style={'fontSize':30, 'textAlign':'center'}),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)

def toURL(mid):
    return image_prefix+mid+".jpg"

def toMid(url):
    return "m"+url.split("/")[-1].split(".")[0]

@app.callback(
    [
    Output(component_id="card01_1",component_property='src'),
    Output(component_id="card02_1",component_property='src'),
    Output(component_id="card03_1",component_property='src'),
    Output(component_id="card04_1",component_property='src'),
    Output(component_id="card05_1",component_property='src'),
    Output(component_id="card06_1",component_property='src'),
    Output(component_id="card07_1",component_property='src'),
    Output(component_id="card08_1",component_property='src')
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
    movieIDs = list(df['MovieID'])[:10]
    ms = [mid[1:] for mid in movieIDs]

    
    #print(image_prefix+movie1+".jpg",image_prefix+movie2+".jpg")
    return toURL(ms[0]),toURL(ms[1]),toURL(ms[2]),toURL(ms[3]),toURL(ms[4]),toURL(ms[5]),toURL(ms[6]),toURL(ms[7])



@app.callback(
    [
    Output(component_id="card01_2i",component_property='src'),
    Output(component_id="card02_2i",component_property='src'),
    Output(component_id="card03_2i",component_property='src'),
    Output(component_id="card04_2i",component_property='src'),
    Output(component_id="card05_2i",component_property='src'),
    Output(component_id="card06_2i",component_property='src'),
    Output(component_id="card07_2i",component_property='src'),
    Output(component_id="card08_2i",component_property='src'),
    Output(component_id="rating1",component_property='value'),
    Output(component_id="rating2",component_property='value'),
    Output(component_id="rating3",component_property='value'),
    Output(component_id="rating4",component_property='value'),
    Output(component_id="rating5",component_property='value'),
    Output(component_id="rating6",component_property='value'),
    Output(component_id="rating7",component_property='value'),
    Output(component_id="rating8",component_property='value'),
    ],
    [
    Input(component_id="Reset",component_property="n_clicks")
    ],
    prevent_initial_call=True,
)   
def reset(_):
    new_sample = np.random.choice(movies_w_ratings,8,replace=False)
    ns = [x[1:] for x in new_sample]
    return toURL(ns[0]),toURL(ns[1]),toURL(ns[2]),toURL(ns[3]),toURL(ns[4]),toURL(ns[5]),toURL(ns[6]),toURL(ns[7]),None,None,None,None,None,None,None,None


@app.callback(
    [
    Output(component_id="warn",component_property='children'),
    Output(component_id="card01_2o",component_property='src'),
    Output(component_id="card02_2o",component_property='src'),
    Output(component_id="card03_2o",component_property='src'),
    Output(component_id="card04_2o",component_property='src'),
    Output(component_id="card05_2o",component_property='src'),
    Output(component_id="card06_2o",component_property='src'),
    Output(component_id="card07_2o",component_property='src'),
    Output(component_id="card08_2o",component_property='src'),
    ],
    [
    Input(component_id="Submit1",component_property="n_clicks")
    ],
    [
    State(component_id="card01_2i",component_property='src'),
    State(component_id="card02_2i",component_property='src'),
    State(component_id="card03_2i",component_property='src'),
    State(component_id="card04_2i",component_property='src'),
    State(component_id="card05_2i",component_property='src'),
    State(component_id="card06_2i",component_property='src'),
    State(component_id="card07_2i",component_property='src'),
    State(component_id="card08_2i",component_property='src'),
    State(component_id="rating1",component_property='value'),
    State(component_id="rating2",component_property='value'),
    State(component_id="rating3",component_property='value'),
    State(component_id="rating4",component_property='value'),
    State(component_id="rating5",component_property='value'),
    State(component_id="rating6",component_property='value'),
    State(component_id="rating7",component_property='value'),
    State(component_id="rating8",component_property='value'),
    ],
   prevent_initial_call=True,
)   
def recsys2(_,url1,url2,url3,url4,url5,url6,url7,url8,r1,r2,r3,r4,r5,r6,r7,r8):
    print(url1)
    print(r1)
    urls = [url1,url2,url3,url4,url5,url6,url7,url8]
    ratings = [r1,r2,r3,r4,r5,r6,r7,r8]
    user_rating = {}
    for i in range(8):
        print(f"i={i}")
        mid = toMid(urls[i])
        r = ratings[i]
        if r is not None:
            user_rating[mid] = int(r)
    if len(user_rating) < 3:
        print("Rate at least 3 movies")
        return "These are some amazing movies that are popular!",toURL("9"),toURL("10"),toURL("11"),toURL("12"),toURL("13"),toURL("14"),toURL("15"),toURL("16")
    ms = []
    rs = []
    for m,r in user_rating.items():
        ms.append(m)
        rs.append(r)
    n_r = len(user_rating)
    test_df = pd.DataFrame({"userID":["new"]*n_r,"itemID":ms,"rating":rs})
    data_train = Dataset.load_from_df(pd.concat([train_df_sampled,test_df]), reader).build_full_trainset()
    algo = KNNWithMeans(sims_options={"user_based":False,"name":"cosine"})
    algo.fit(data_train)

    res = {}
    for movie in movies_id:
        if movie in user_rating:
            continue
        cur = algo.predict('new',movie)
        res[movie] = cur[3]
    rl = [x[1][1:] for x in sorted([(r,m) for m,r in res.items()])[-10:][::-1]]
    print(rl)
    return "",toURL(rl[0]),toURL(rl[1]),toURL(rl[2]),toURL(rl[3]),toURL(rl[4]),toURL(rl[5]),toURL(rl[6]),toURL(rl[7]),





if __name__ == "__main__":
    app.run(debug=True)
