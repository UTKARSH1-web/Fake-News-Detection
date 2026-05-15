def detect_news(score):

    if score > 0.35:
        return "✅ Likely Real News"

    elif score > 0.20:
        return "⚠️ Partially Verified News"

    else:
        return "🚫 Likely Fake News"