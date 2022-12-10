import pickle
import numpy as np
import pandas as pd

ratings = pd.read_table("https://liangfgithub.github.io/MovieData/ratings.dat",sep="::",header=None,engine='python')
ratings.columns = ['UserID','MovieID','Rating','Timestamp']
ratings['UserID'] = ratings['UserID'].apply(lambda x:'u'+str(x))
ratings['MovieID'] = ratings['MovieID'].apply(lambda x:'m'+str(x))
movies_id = list(ratings['MovieID'].unique())

with open('movies_w_ratings.pickle', 'wb') as handle:
    pickle.dump(movies_id, handle)

movies = pd.read_table("https://liangfgithub.github.io/MovieData/movies.dat",sep="::",header=None,engine='python',encoding='latin-1')
#movies0 = movies.copy()
movies.columns = ['MovieID','Title','Genres']

#movies0 = movies.copy()
movies['year'] = movies['Title'].apply(lambda x:int(x[-5:-1]))
movies['MovieID'] = movies['MovieID'].apply(lambda x:'m'+str(x))
movies0 = movies.copy()
movies['Genres'] = movies['Genres'].apply(lambda x:x.split("|"))
movies_w_ratings = movies.explode('Genres').merge(ratings,on='MovieID',how='left')
movies = None

sys1_data = movies_w_ratings.groupby(['Genres','MovieID','Title']).agg({'UserID':'count','Rating':np.mean,'year':'first'}).rename(columns={'UserID':'numRatings'}).reset_index().set_index('Genres')

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

genres = movies_w_ratings['Genres'].unique()
sys1_result = {}
for genre in sys1_data.index.unique():
    for method in ['Rating','Popularity']:
        sys1_result[genre,method] = system1(genre,method,sys1_data)
with open('sys1_result.pickle', 'wb') as handle:
    pickle.dump(sys1_result, handle)