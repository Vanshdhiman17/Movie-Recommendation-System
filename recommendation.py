import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_movies = pd.read_csv("movies.csv")
print(df_movies.head())
print(f"Columns are {df_movies.shape[0]} and Rows are {df_movies.shape[1]}")
print(df_movies.describe())
print(df_movies.isnull().sum())
print(df_movies.info())
print(df_movies['title'].value_counts().sum())

df_rating = pd.read_csv("ratings.csv")
print(df_rating.head())
print(f"Columns are {df_rating.shape[0]} and Rows are {df_rating.shape[1]}")
print(df_rating.describe())
print(df_rating.isnull().sum())
print(df_rating.info())

df_user = pd.read_csv("users.csv")
print(df_user.head())
print(f"Columns are {df_user.shape[0]} and Rows are {df_user.shape[1]}")
print(df_user.describe())
print(df_user.isnull().sum())
print(df_user.info())

print("Total number of movies are : ", df_movies['movieId'].value_counts().sum())
print("Total number of users are : ", df_user['userId'].value_counts().sum())
print("Total number of ratings are : ", df_rating['rating'].value_counts().sum())
print("Different types of ratings present in the dataset are : \n", df_rating['rating'].value_counts().sort_index())

df_rating['rating'].value_counts().sort_index().plot(kind='bar', figsize=(7,5))
plt.xlabel("rating")
plt.ylabel("number of ratings")
plt.title("distribution of ratings")

top_movies = (df_rating.groupby('movieId').size().sort_values(ascending=False).head(20).reset_index(name="ratingCount"))
top_movies = top_movies.merge(df_movies[['movieId', 'title']],on='movieId')
print(top_movies)

top_movies.sort_values('ratingCount').plot(x='movieId',y='ratingCount',kind='barh',figsize=(10, 9))
plt.xlabel("Number of Ratings")
plt.ylabel("Movie ID")
plt.tight_layout()
plt.title("Top 20 Most Rated Movies")

sparsity = 1 - (df_rating['rating'].value_counts().sum())/(df_user['userId'].value_counts().sum() * df_movies['movieId'].value_counts().sum())
print(round(sparsity * 100,2))

print("average rating : ",round(df_rating['rating'].mean(),2))
print("median rating : ", df_rating['rating'].median())
print("Rating with highest frequency : ", df_rating['rating'].value_counts().idxmax())
print("Rating high percentage : ", round((df_rating['rating'] >= 4).mean()*100, 2))
print("Rating low percentage : ", round((df_rating['rating'] <= 2).mean()*100, 2))

movie_rating = df_rating.groupby('movieId').size().reset_index(name='rating_count')
movie_rating = movie_rating.merge(df_movies[['movieId', 'title']], on='movieId')
print(movie_rating)

df = pd.DataFrame(movie_rating)
print(df.head())
less_than_10 = (movie_rating['rating_count']<10).sum()
print("total number of movies less than the rating of 10 : ",less_than_10)

print("Total no of movies watched by each user is \n",(df_rating['userId'].value_counts().sort_index()).head(10))
print("average ratings per user : \n", (df_rating['userId'].value_counts().sort_index()).mean())
print("most active users are \n", df_rating['userId'].value_counts().sort_values(ascending=False).head(10))

total_movies = df_rating['movieId'].nunique()
user_coverage = df_rating['userId'].value_counts().sort_index()/ total_movies * 100
print("content coverage as per the user \n", user_coverage.sort_values(ascending=False).head(10))

user_rating_count = df_rating.groupby('userId')['movieId'].count()
user_avg_rating = df_rating.groupby('userId')['rating'].mean()
user_stats = pd.DataFrame({'rating_count': user_rating_count,'avg_rating': user_avg_rating})
print(user_stats.head())
plt.figure(figsize=(5,5))
sns.heatmap(user_stats.corr(numeric_only=True), annot=True)
plt.figure(figsize=(5,5))
plt.scatter(user_stats['rating_count'],user_stats['avg_rating'])
plt.xlabel("Number of Ratings")
plt.ylabel("Average Rating")
plt.title("User Activity vs Average Rating")

print("no of males and females are \n", df_user['gender'].value_counts())

user_rating = pd.merge(df_rating, df_user, on="userId")
avg_gender_rating = user_rating.groupby('gender')['rating'].mean()
print(round(avg_gender_rating, 2))

plt.figure(figsize=(5,5))
sns.barplot(data=user_rating, x='gender', y='rating')
plt.title("average rating")

print("users with different ages are \n", df_user['age'].value_counts())
plt.figure(figsize=(5,5))
df_user['age'].value_counts().plot(kind='barh')
plt.xlabel("no of users")
plt.ylabel("age")
plt.title("users with different ages")
print("top 3 ages with most users  \n", df_user['age'].value_counts().sort_values(ascending=False).head(3))

age_rating = pd.merge(df_rating, df_user, on="userId")
avg_age_rating = age_rating.groupby('age')['rating'].mean().sort_values(ascending=False).head(3)
print("top 3 age with highest average rating \n", round(avg_age_rating,2))

plt.figure(figsize=(5,5))
sns.barplot(x=avg_age_rating.index, y=avg_age_rating.values, palette='rainbow')
print("top 10 occupations with most users \n", df_user['occupation'].value_counts().sort_values(ascending=False).head(10))

occupation_data = pd.merge(df_user, df_rating, on="userId")
avg_occ_rating = round(occupation_data.groupby('occupation')['rating'].mean().sort_values(ascending=False).head(10), 2)
print("top 10 occupation with highest average ratings \n",avg_occ_rating)

df_movies = df_movies.assign(genres = df_movies['genres'].str.split('|')).explode('genres')
print("total no of genres \n", df_movies['genres'].value_counts())
print("genre with most movies : ", df_movies['genres'].value_counts().idxmax())
print("top 5 most watched genres are \n", df_movies['genres'].value_counts().head())

rating_movies = pd.merge(df_rating, df_movies, on="movieId")
rating_genres = rating_movies.assign(genres = rating_movies['genres'].str.split("|")).explode('genres')
print("rating per genre \n", rating_genres['genres'].value_counts())
print("genre recieving most ratings : ", rating_genres['genres'].value_counts().idxmax())
plt.figure(figsize=(10,8))
sns.barplot(x=rating_genres['genres'].value_counts().index, y=rating_genres['genres'].value_counts().values, palette='Set2',hue=rating_genres['genres'].value_counts().index)
plt.xlabel("genre")
plt.ylabel("no of ratings")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.title("no of ratings by genre")

avg_genre_rating = rating_genres.groupby('genres')['rating'].mean().sort_values(ascending = False)
print(round(avg_genre_rating,2))

five_star = rating_genres[rating_genres['rating'] == 5]
five_star_count = (five_star['genres'].value_counts().sort_values(ascending = False))
print("top 5 genres with 5 star rating \n",five_star_count.head())

plt.figure(figsize=(7,5))
sns.barplot(x=five_star_count.head().values, y=five_star_count.head().index, hue=five_star_count.head().values, palette='Paired')
plt.xlabel("no of 5 star rating")
plt.ylabel("genre")
plt.title("top 5 genre with 5 star rating")


df_movies["year"] = df_movies["title"].str.extract(r"\((\d{4})\)")
df_movies["year"] = pd.to_numeric(df_movies["year"], errors="coerce")
print(df_movies[["title", "year"]].head())
movies_per_year = df_movies['year'].value_counts().sort_values(ascending=False).head()
print("movies per year \n", movies_per_year)
plt.figure(figsize=(6,7))
movies_per_year.plot(kind = "line", marker = "o")
plt.xlabel("released year")
plt.ylabel("no of movies")
plt.title("no of movies released per year")
plt.xticks(rotation=45)

rating_movie = pd.merge(df_movies, df_rating, on="movieId")

rating_per_year = rating_movie.groupby('year')['rating'].value_counts().sort_values(ascending=False)
print(rating_per_year.head())
plt.figure(figsize=(6,6))
correlation = rating_movie[['year', 'rating']].corr().loc['year', 'rating']
sns.heatmap(rating_movie.corr(numeric_only=True), annot=True)

user_rating = pd.merge(user_rating, df_movies, on="movieId")
user_genre = user_rating.assign(genres = user_rating['genres'].str.split("|")).explode('genres')
print(user_genre.head())

user_genre_counts = (user_genre.groupby(["userId", "genres"]).size().reset_index(name="Rating_Count"))
user_preferred_genre = (user_genre_counts.sort_values(["userId", "Rating_Count"],ascending=[True, False]).drop_duplicates("userId"))
print("genre preferred by each user \n",user_preferred_genre.head())

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

df_moviess = pd.read_csv("movies.csv")
print(df_moviess.head())
df_moviess['genre_list'] = df_moviess['genres'].str.split('|')
print(df_moviess.head())
mlb = MultiLabelBinarizer()
genre_matrix = mlb.fit_transform(df_moviess['genre_list'])
print(mlb.classes_)
similarity_matrix = cosine_similarity(genre_matrix)
print(similarity_matrix.shape)
print(similarity_matrix[0])

movie_indices = pd.Series(df_moviess.index, index = df_moviess['title']).drop_duplicates()
print(movie_indices)


def recommend_movies(movie_title, n=10):
    movie_title = movie_title.lower()
    matches = df_moviess[df_moviess['title'].str.lower().str.contains(movie_title, na=False)]
    if matches.empty:
        print("Movie Not Found")
    idx = matches.index[0]
    scores = similarity_matrix[idx]
    similar_movies = scores.argsort()[::-1][1:n+1]
    return df_moviess.iloc[similar_movies][["title", "genres"]]

