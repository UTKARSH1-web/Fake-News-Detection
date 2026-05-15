import streamlit as st

from src.fetch_news import get_news
from src.similarity import calculate_similarity
from src.detector import detect_news

# PAGE CONFIG
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

/* IMPORT FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* FULL PAGE */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */
.stApp {

    background:
    radial-gradient(circle at top left, rgba(0,180,255,0.15), transparent 25%),
    radial-gradient(circle at bottom right, rgba(255,0,150,0.12), transparent 25%),
    linear-gradient(135deg, #050816 0%, #0b132b 40%, #1c2541 100%);

    color: white;
}

/* WORLD MAP EFFECT */
.stApp::before {

    content: "";

    position: fixed;

    top: 0;
    left: 0;

    width: 100%;
    height: 100%;

    background-image:
    url("https://www.transparenttextures.com/patterns/cubes.png");

    opacity: 0.08;

    z-index: 0;
}

/* CONTAINER */
.block-container {

    position: relative;
    z-index: 1;

    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* TITLE */
.main-title {

    text-align: center;

    font-size: 58px;

    font-weight: 700;

    color: white;

    margin-bottom: 10px;

    text-shadow: 0px 0px 20px rgba(0,255,255,0.4);
}

/* SUBTITLE */
.subtitle {

    text-align: center;

    color: #d6d6d6;

    font-size: 20px;

    margin-bottom: 35px;
}

/* TEXT AREA */
.stTextArea textarea {

    background: rgba(255,255,255,0.08) !important;

    color: white !important;

    border-radius: 18px !important;

    border: 1px solid rgba(255,255,255,0.15) !important;

    font-size: 18px !important;

    padding: 15px !important;

    backdrop-filter: blur(10px);
}

/* BUTTON */
.stButton button {

    background: linear-gradient(
        90deg,
        #00c6ff,
        #0072ff
    ) !important;

    color: white !important;

    border-radius: 15px !important;

    height: 3.4em;

    width: 100%;

    font-size: 18px;

    font-weight: 600;

    border: none !important;

    transition: 0.3s ease;
}

/* BUTTON HOVER */
.stButton button:hover {

    transform: scale(1.02);

    box-shadow: 0px 0px 20px rgba(0,198,255,0.5);
}

/* RESULT BOX */
.result-box {

    background: rgba(255,255,255,0.08);

    border: 1px solid rgba(255,255,255,0.1);

    backdrop-filter: blur(12px);

    padding: 30px;

    border-radius: 22px;

    text-align: center;

    font-size: 34px;

    font-weight: 700;

    color: white;

    margin-top: 25px;

    margin-bottom: 30px;

    box-shadow: 0px 0px 30px rgba(0,0,0,0.3);
}

/* NEWS CARD */
.news-card {

    background: rgba(255,255,255,0.08);

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    padding: 22px;

    border-radius: 18px;

    margin-bottom: 18px;

    transition: 0.3s ease;
}

/* CARD HOVER */
.news-card:hover {

    transform: translateY(-5px);

    box-shadow: 0px 0px 25px rgba(0,198,255,0.2);
}

/* NEWS TITLE */
.news-title {

    color: white;

    font-size: 22px;

    font-weight: 600;

    line-height: 1.5;
}

/* NEWS SOURCE */
.news-source {

    color: #cfcfcf;

    margin-top: 12px;

    font-size: 15px;
}

/* SECTION TITLE */
.section-title {

    font-size: 30px;

    font-weight: 700;

    color: white;

    margin-top: 30px;

    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    '<div class="main-title">🌍 Real-Time Fake News Detector</div>',
    unsafe_allow_html=True
)

# SUBTITLE
st.markdown(
    '<div class="subtitle">AI-powered live news verification using NLP & real-time internet sources</div>',
    unsafe_allow_html=True
)

# INPUT
user_input = st.text_area(
    "Enter News Headline",
    placeholder="Example: Scientists discover aliens on Mars"
)

# BUTTON
if st.button("🔍 Verify News"):

    if user_input.strip() == "":
        st.warning("Please enter a news headline")

    else:

        with st.spinner("Scanning global news sources..."):

            articles = get_news(user_input)

        if len(articles) == 0:

            st.error("No related news found")

        else:

            score = calculate_similarity(user_input, articles)

            result = detect_news(score)

            # RESULT BOX
            st.markdown(
                f'''
                <div class="result-box">
                    {result}
                </div>
                ''',
                unsafe_allow_html=True
            )

            # SCORE
            st.markdown(
                '<div class="section-title">📊 Confidence Score</div>',
                unsafe_allow_html=True
            )

            progress_val = max(0.0, min(float(score), 1.0))

            st.progress(progress_val)

            st.write(
                f"### {round(score * 100, 2)}% Match Found"
            )

            # ARTICLES
            st.markdown(
                '<div class="section-title">🌐 Related Global News</div>',
                unsafe_allow_html=True
            )

            for article in articles:

                st.markdown(
                    f'''
                    <div class="news-card">

                        <div class="news-title">
                            {article['title']}
                        </div>

                        <div class="news-source">
                            📰 Source: {article['source']}
                        </div>

                    </div>
                    ''',
                    unsafe_allow_html=True
                )