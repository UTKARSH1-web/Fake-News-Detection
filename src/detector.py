def detect_news(score):
    """
    Classify news based on composite similarity score.
    Uses calibrated thresholds for the multi-signal composite scoring system.
    """

    if score > 0.25:
        return "✅ Likely Real News"

    elif score > 0.12:
        return "⚠️ Partially Verified News"

    else:
        return "🚫 Likely Fake News"