import streamlit as st
import pandas as pd
import pickle
import requests
from requests.exceptions import RequestException

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a89bd48535fad9d4ec39ea960111a56b&language=en-US'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
    except RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500"  # Placeholder image in case of error

def recommend_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        # fetching poster
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load the movie list and similarity matrix
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender Buddy')

selected_movie_name = st.selectbox(
    "Which movie have you watched?",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations, posters = recommend_movies(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommendations[idx])
            st.markdown(
                f'<a href="https://www.google.com/search?q={recommendations[idx]}+movie"><img src="{posters[idx]}" width="100"></a>',
                unsafe_allow_html=True
            )
