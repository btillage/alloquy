import openai
import requests

# OpenAI setup
def setup_openai_api():
    openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_gpt3_response(message):
    setup_openai_api()
    response = openai.Completion.create(engine="davinci", prompt=message, max_tokens=150)
    return response.choices[0].text.strip()

# Fetch Daily Quotes from ZenQuotes API
def get_daily_quote():
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        quote_data = response.json()[0]
        return f"{quote_data['q']} - {quote_data['a']}"
    else:
        return "No quote available."

# Twinword Sentiment Analysis
def get_sentiment_twinword(text):
    api_key = 'YOUR_TWINWORD_API_KEY'  # Replace with your Twinword API key
    url = 'https://twinword-sentiment-analysis.p.rapidapi.com/analyze/'
    headers = {'x-rapidapi-host': "twinword-sentiment-analysis.p.rapidapi.com",
               'x-rapidapi-key': api_key}
    payload = {'text': text}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        result = response.json()
        return result['type']
    else:
        return "Error"

# User Profile
class UserProfile:
    def __init__(self):
        self.preferences = {}

    def update_preference(self, user, key, value):
        if user not in self.preferences:
            self.preferences[user] = {}
        self.preferences[user][key] = value

    def get_preference(self, user, key):
        return self.preferences.get(user, {}).get(key, None)

user_profiles = UserProfile()

# Main response function
def get_response(user_input, user):
    sentiment = get_sentiment_twinword(user_input)
    user_profiles.update_preference(user, 'last_sentiment', sentiment)
    
    response = get_gpt3_response(user_input)
    return response