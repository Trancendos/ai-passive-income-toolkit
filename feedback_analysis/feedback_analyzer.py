import openai
import os

class FeedbackAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of a given text.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert."},
                    {"role": "user", "content": f"Analyze the sentiment of the following text and return one of the following: Positive, Negative, or Neutral.\n\nText: \"{text}\""}
                ],
                max_tokens=10,
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"

    def identify_key_themes(self, feedback_list):
        """
        Identifies key themes from a list of feedback entries.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in text analysis and theme identification."},
                    {"role": "user", "content": f"Identify the key themes from the following list of user feedback. Group similar feedback together and provide a summary of the main topics.\n\nFeedback:\n- {'\n- '.join(feedback_list)}"}
                ],
                max_tokens=500,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    # Example usage
    analyzer = FeedbackAnalyzer()

    # Sample feedback data
    feedback_data = [
        "The app is amazing! So easy to use and very intuitive.",
        "I'm having trouble with the login. It keeps crashing on my device.",
        "The new update is a bit confusing. I can't find the settings menu anymore.",
        "Billing is incorrect. I was charged twice for my subscription.",
        "Love the new features, especially the dark mode. Keep up the great work!",
        "Customer support was very helpful and resolved my issue quickly."
    ]

    print("--- Sentiment Analysis ---")
    for feedback in feedback_data:
        sentiment = analyzer.analyze_sentiment(feedback)
        print(f"'{feedback}' -> Sentiment: {sentiment}")

    print("\n--- Key Theme Identification ---")
    themes = analyzer.identify_key_themes(feedback_data)
    print(themes)
