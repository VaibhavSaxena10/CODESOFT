import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv") 
movies = movies.head(10000)

for col in ["genres", "description"]:
    if col in movies.columns:
        movies[col] = movies[col].fillna("")
    else:
        movies[col] = "" 

def combine_features(row):
    return f"{row['title']} {row['genres']} {row['description']}"


movies["combined_features"] = movies.apply(combine_features, axis=1)


tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["combined_features"])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

movies = movies.reset_index()
indices = pd.Series(movies.index, index=movies["title"].str.lower())

def get_recommendations(title, top_n=5):
    """
    Given a movie title, return top_n similar movies based on cosine similarity.
    """
    title = title.lower()

    if title not in indices:
        print("Movie not found in database.")
        return []

    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    return movies["title"].iloc[movie_indices].tolist()

def run_recommender():
    print("Welcome to the Movie Recommendation System!")
    print("Type a movie title to get similar movie suggestions.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter movie title: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting recommendation system. Goodbye!")
            break

        recommendations = get_recommendations(user_input, top_n=5)
        if recommendations:
            print("\nRecommended movies similar to:", user_input)
            for i, movie_title in enumerate(recommendations, start=1):
                print(f"{i}. {movie_title}")
            print()
        else:
            print("No recommendations found (movie may not exist in dataset).\n")


if __name__ == "__main__":
    run_recommender()
