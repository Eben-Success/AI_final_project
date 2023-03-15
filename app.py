import streamlit as st
import pandas as pd
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

# Load data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Load Image
image = Image.open('stars-movie.jpg')

# Merge movies and ratings data
movie_ratings = pd.merge(movies, ratings)

# Create pivot table
ratings_matrix = movie_ratings.pivot_table(index='userId', columns='title', values='rating')

# Fill NaN values with 0
ratings_matrix.fillna(0, inplace=True)

# Calculate cosine similarity
cosine_sim = cosine_similarity(ratings_matrix)

# Define function to get similar movies
def get_similar_movies(movie_title, cosine_sim, ratings_matrix):
    movie_idx = ratings_matrix.columns.get_loc(movie_title)
    movie_scores = list(enumerate(cosine_sim[movie_idx]))
    movie_scores = sorted(movie_scores, key=lambda x: x[1], reverse=True)
    movie_scores = movie_scores[1:11]
    movie_indices = [i[0] for i in movie_scores]
    return movie_indices

# Streamlit app
st.title('Movie Recommender System')

st.image(image, width=700)

# Dropdown for selecting movie
movie_list = ratings_matrix.columns.tolist()
selected_movie = st.selectbox('Select a movie:', movie_list)

# Button to get similar movies
if st.button('Get similar movies'):
    similar_movies = get_similar_movies(selected_movie, cosine_sim, ratings_matrix)
    st.write('Top 10 similar movies to', selected_movie, ':')
    st.write(movies['title'].iloc[similar_movies])
