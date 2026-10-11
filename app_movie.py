import streamlit as st
from recommendation import recommend_movies, df_moviess

st.set_page_config(
    page_title="MovieRecs",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top right, #211747, #0b0e19 55%);
    color: #f5f6ff;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #192235, #111827);
    border-right: 1px solid #29344c;
}
h1, h2, h3, p, label {
    color: #f5f6ff;
}
.movie-card {
    background: linear-gradient(145deg, #202b40, #171d2d);
    border: 1px solid #394763;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
    min-height: 220px;
}
.poster {
    background: #292344;
    border-radius: 10px;
    height: 95px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 45px;
    margin-bottom: 12px;
}
.movie-title {
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 8px;
}
.genre {
    display: inline-block;
    background: #344c91;
    color: white;
    padding: 4px 8px;
    border-radius: 15px;
    font-size: 11px;
    margin: 3px 2px 0 0;
}
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background: #20283a;
    color: white;
    border-radius: 10px;
    min-height: 42px;
}
.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(90deg, #7558f5, #6955e9);
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 42px;
    font-weight: bold;
}
.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #8b75ff;
    color: white;
}
hr {
    border-color: #303b52;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(
        "# 🎬 Movie<span style='color:#8b75ff'>Recs</span>",
        unsafe_allow_html=True
    )
    st.caption("Find your next favorite movie!")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Home", "Get Recommendations", "About"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### About This App")
    st.write(
        "Discover similar movies using content-based filtering "
        "and movie genres."
    )

    st.markdown("### 💡 How it works")
    st.write(
        "1. Enter a movie name\n\n"
        "2. Choose the number of movies\n\n"
        "3. Discover similar movies"
    )

# Main heading
st.markdown("# 🍿 Movie Recommendation System")
st.markdown(
    '<p style="color:#a5b2cc;font-size:18px;">'
    'Discover movies you’ll love, based on their similarity!'
    '</p>',
    unsafe_allow_html=True
)

# Home and Recommendations
if page in ["Home", "Get Recommendations"]:

    with st.container(border=True):
        st.markdown("### Enter a movie name")

        with st.form("movie_form"):
            col1, col2 = st.columns([3, 1], gap="medium")

            with col1:
                st.markdown("**Movie title**")
                movie = st.text_input(
                    "Movie",
                    placeholder="e.g. Toy Story, Inception, Avengers...",
                    label_visibility="collapsed"
                )

            with col2:
                st.markdown("**Number of movies**")
                number = st.selectbox(
                    "Count",
                    [5, 10, 15, 20],
                    index=0,
                    label_visibility="collapsed"
                )

            st.write("")

            search = st.form_submit_button(
                "🔍 Get Recommendations",
                use_container_width=True
            )

        st.caption(
            "💡 Enter a movie name and select how many recommendations you want."
        )

    # Search and recommend
    if search:
        if not movie.strip():
            st.warning("Please enter a movie name.")
        else:
            results = recommend_movies(movie.strip(), n=number)

            if results is None or results.empty:
                st.error("Movie not found. Please try another title.")
                st.session_state.pop("results", None)
                st.session_state.pop("searched_movie", None)
            else:
                st.session_state["results"] = results
                st.session_state["searched_movie"] = movie.strip()

    # Display recommendation cards
    if "results" in st.session_state:
        st.markdown("## ⭐ Recommended Movies")
        st.markdown(
            f"Top recommendations for: "
            f"**{st.session_state['searched_movie']}**"
        )

        results = st.session_state["results"]

        for start in range(0, len(results), 5):
            cols = st.columns(5)
            batch = results.iloc[start:start + 5]

            for col, (_, row) in zip(cols, batch.iterrows()):
                with col:
                    genres = str(row["genres"]).split("|")
                    tags = "".join(
                        f'<span class="genre">{genre}</span>'
                        for genre in genres[:4]
                    )

                    title = row["title"]

                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <div class="poster">🎬</div>
                            <div class="movie-title">{title}</div>
                            <div>{tags}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# About page
elif page == "About":
    st.markdown("## About MovieRecs")
    st.write(
        "MovieRecs is a movie recommendation application "
        "built using the MovieLens dataset."
    )

    st.markdown("### Technologies")
    st.write(
        "- Python\n"
        "- Pandas\n"
        "- Scikit-learn\n"
        "- Streamlit\n"
        "- Content-based filtering\n"
        "- Cosine similarity"
    )

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#71809e;">'
    'Built with ❤️ using Streamlit'
    '</p>',
    unsafe_allow_html=True
)
