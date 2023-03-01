import streamlit as st
import pickle
import pandas as pd
import sklearn
import requests
from sklearn.metrics.pairwise import cosine_similarity
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7ce8d5eda5fdcf164320f587eff660c6&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

vectors = pickle.load(open(r"C:\Users\harsh\Downloads\vectors.pkl",
                           'rb'))
similarity = cosine_similarity(vectors)
movies_list = pickle.load(open(r"C:\Users\harsh\Downloads\movies.pkl",
                               'rb'))
movies_list = movies_list['title'].values
movie_final_data = pd.read_csv(r"C:\Users\harsh\Downloads\Movies_TMDB.csv")


def recommend(movies):
    indexes = movie_final_data[movie_final_data['title'] == movies].index[0]
    distances = similarity[indexes]
    top_5_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in top_5_list:
        movie_id = movie_final_data['movie_id'].iloc[i[0]]
        recommended_movies.append(movie_final_data['title'].iloc[i[0]])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title("Movies Recommendation System")

selected_movie = st.selectbox('Which movie you selected',
                    movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


