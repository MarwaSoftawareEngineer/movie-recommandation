import pickle  # Importation du module pickle pour la sérialisation des données
import streamlit as st  # Importation de la bibliothèque Streamlit pour la création d'applications web interactives
import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP

# Fonction pour récupérer l'affiche d'un film
def fetch_poster(movie_id):
    # Construction de l'URL pour récupérer les données du film à partir de son ID
    url = "https://api.themoviedb.org/3/movie/{}?api_key=919fe932ba5864ddf8c7b5d80a7f4f9d&language=en-US".format(movie_id)
    # Envoi d'une requête GET à l'API
    data = requests.get(url)
    # Conversion de la réponse en format JSON
    data = data.json()
    # Récupération du chemin de l'affiche du film
    poster_path = data['poster_path']
    # Construction du chemin complet de l'affiche
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Fonction pour recommander des films
def recommend(movie):
    # Récupération de l'index du film dans le DataFrame 'movies'
    index = movies[movies['title'] == movie].index[0]
    # Tri des similarités pour obtenir les films recommandés
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    # Boucle pour récupérer les informations des films recommandés
    for i in distances[1:6]:
        # Récupération de l'ID du film
        movie_id = movies.iloc[i[0]].movie_id
        # Appel de la fonction pour récupérer l'affiche du film
        recommended_movie_posters.append(fetch_poster(movie_id))
        # Récupération du nom du film recommandé
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Entête de l'application Streamlit
st.title('Movie Recommendation System')

# Chargement des données des films et de la matrice de similarité
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Menu déroulant pour sélectionner un film
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

# Bouton pour afficher les recommandations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    # Affichage des recommandations en colonnes
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], width=150)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], width=150)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], width=150)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], width=150)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], width=150)

# Ajout du fond d'écran
st.markdown(
    """
    <style>
    body {
        background-image: url("https://th.bing.com/th/id/OIP.1-jretDM6phD3x2QgWqKowHaHa?rs=1&pid=ImgDetMain");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)