import streamlit as st
import os

st.title("News Summarization & Sentiment Analysis")

company_name = st.text_input("Enter Company Name:")

if st.button("Fetch News"):
    news_articles = fetch_news(company_name)
    for article in news_articles:
        st.subheader(article["title"])
        st.write(f"[Read More]({article['link']})")
        
        summary = summarize_article(article["title"])
        sentiment = analyze_sentiment(summary)
        st.write(f"**Summary:** {summary}")
        st.write(f"**Sentiment:** {sentiment}")

    report = compare_articles(news_articles)
    st.write("### Sentiment Analysis Report")
    st.json(report)

    st.write("### Generating Hindi Speech...")
    speech_file = text_to_speech_hindi(f"{company_name} ka samachar...")
    st.audio(speech_file, format="audio/mp3")
