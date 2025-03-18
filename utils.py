import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from gtts import gTTS
import os

# Download the VADER lexicon for sentiment analysis
nltk.download("vader_lexicon")

# Initialize NLP Models
summarizer = pipeline("summarization")
sia = SentimentIntensityAnalyzer()

def fetch_news(company_name):
    """
    Fetches news articles related to the given company from Google News.
    Returns a list of dictionaries with title and link.
    """
    url = f"https://news.google.com/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select(".DY5T1d")[:10]:  # Extract 10 news items
        title = item.get_text()
        link = "https://news.google.com" + item["href"][1:]
        articles.append({"title": title, "link": link})

    return articles

def summarize_article(text):
    """
    Summarizes the given text using a pre-trained summarization model.
    """
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

def analyze_sentiment(text):
    """
    Analyzes sentiment of a given text and returns Positive, Neutral, or Negative.
    """
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

def compare_articles(articles):
    """
    Compares sentiment distribution across multiple articles.
    Returns a summary of sentiment trends.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    topics = set()

    for article in articles:
        sentiment_counts[article["sentiment"]] += 1
        topics.update(article.get("topics", []))

    return {
        "sentiment_distribution": sentiment_counts,
        "topics": list(topics),
    }

def text_to_speech_hindi(text, filename="output.mp3"):
    """
    Converts given text to Hindi speech and saves it as an audio file.
    """
    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
    return filename

def format_output(company_name, articles):
    """
    Formats the final structured JSON output for the application.
    """
    final_output = {
        "Company": company_name,
        "Articles": [],
        "Comparative Sentiment Score": None,
        "Final Sentiment Analysis": "",
        "Audio": None
    }

    for article in articles:
        summary = summarize_article(article["title"])
        sentiment = analyze_sentiment(summary)
        
        final_output["Articles"].append({
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": ["Business", "Finance", "Tech"]  # Placeholder topics
        })

    comparative_report = compare_articles(final_output["Articles"])
    final_output["Comparative Sentiment Score"] = comparative_report
    final_output["Final Sentiment Analysis"] = f"{company_name} news has a mixed sentiment trend."
    
    speech_text = f"{company_name} ka samachar: {comparative_report['sentiment_distribution']}"
    final_output["Audio"] = text_to_speech_hindi(speech_text)

    return final_output
