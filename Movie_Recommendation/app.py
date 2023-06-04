
import pandas as pd
import numpy as np
from ast import literal_eval

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cosine_sim


credits_df = pd.read_csv("./tmdb_5000_credits.csv")
movies_df = pd.read_csv("./tmdb_5000_movies.csv")
# print(movies_df.head())
# print(credits_df.head())
credits_df.columns = ['id', 'title', 'cast', 'crew']
movies_df = movies_df.merge(credits_df, on="id")
# print(movies_df.head())

features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(literal_eval)

# print(movies_df[features].head(10))


def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan


def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []


movies_df["director"] = movies_df["crew"].apply(get_director)
features = ["cast", "keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(get_list)

# print(movies_df[['title', 'cast', 'director', 'keywords', 'genres']].head())


def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""


features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    movies_df[feature] = movies_df[feature].apply(clean_data)


def create_soup(features):
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' + ' '.join(features['genres'])


movies_df["soup"] = movies_df.apply(create_soup, axis=1)

# print(movies_df["soup"].head())

count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(movies_df["soup"])
# print(count_matrix.shape)

cosine_sim2 = cosine_sim(count_matrix, count_matrix)
print(cosine_sim2.shape)

movies_df = movies_df.reset_index()
indices = pd.Series(movies_df.index, index=movies_df['original_title'])

indices = pd.Series(
    movies_df.index, index=movies_df["original_title"]).drop_duplicates()


# print(indices.head())


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:11]
    # (a, b) where a is id of movie, b is similarity_scores
    movies_indices = [ind[0] for ind in similarity_scores]
    movies = movies_df["original_title"].iloc[movies_indices]
    return movies


print("################ Content Based System #############")
print("Recommendations for The Dark Knight Rises")
print(get_recommendations("The Dark Knight Rises", cosine_sim2))
print()
print("Recommendations for The Amazing Spider-Man")
print(get_recommendations("The Amazing Spider-Man", cosine_sim2))
