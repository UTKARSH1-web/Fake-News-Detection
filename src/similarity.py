from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(user_news, articles):

    article_titles = [article["title"] for article in articles]

    all_texts = [user_news] + article_titles

    try:
        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(all_texts)
        similarity_scores = cosine_similarity(matrix[0:1], matrix[1:])
        max_score = similarity_scores.max()
        return max_score
    except ValueError:
        return 0.0