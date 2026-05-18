from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(user_news, articles):
    """
    Calculate a composite similarity score between user input and fetched articles.
    Uses both titles and descriptions with n-gram TF-IDF for better phrase matching.
    Returns a composite score combining multiple signals.
    """

    # Build comparison texts: combine title + description for each article
    article_texts = []
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        combined = f"{title} {description}".strip()
        if combined:
            article_texts.append(combined)

    if not article_texts:
        return 0.0

    all_texts = [user_news] + article_texts

    try:
        # Use 1-2 gram TF-IDF for better phrase matching
        tfidf = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=10000
        )
        matrix = tfidf.fit_transform(all_texts)

        # Compute similarity of user input against all articles
        similarity_scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

        # --- Multi-signal scoring ---

        # Signal 1: Max similarity score (best single match)
        max_score = float(similarity_scores.max())

        # Signal 2: Average of top-3 scores (consistency of matches)
        sorted_scores = sorted(similarity_scores, reverse=True)
        top_3 = sorted_scores[:min(3, len(sorted_scores))]
        avg_top3 = sum(top_3) / len(top_3)

        # Signal 3: Coverage — how many articles have at least some match
        match_threshold = 0.05
        matching_count = sum(1 for s in similarity_scores if s > match_threshold)
        coverage_ratio = matching_count / len(similarity_scores)

        # Composite score: weighted combination
        # 40% best match + 35% top-3 average + 25% coverage
        composite = (0.40 * max_score) + (0.35 * avg_top3) + (0.25 * coverage_ratio)

        return composite

    except ValueError:
        return 0.0