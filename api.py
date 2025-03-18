from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/fetch_news", methods=["GET"])
def fetch_news_api():
    company = request.args.get("company")
    news = fetch_news(company)
    return jsonify(news)

@app.route("/analyze_sentiment", methods=["POST"])
def sentiment_api():
    data = request.json
    sentiment = analyze_sentiment(data["text"])
    return jsonify({"sentiment": sentiment})

if __name__ == "__main__":
    app.run(debug=True)
