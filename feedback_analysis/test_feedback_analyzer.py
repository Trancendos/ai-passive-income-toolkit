import unittest
from unittest.mock import patch, MagicMock
from feedback_analyzer import FeedbackAnalyzer

class TestFeedbackAnalyzer(unittest.TestCase):
    @patch('feedback_analyzer.openai.ChatCompletion.create')
    def test_analyze_sentiment(self, mock_create):
        # Mock the API response for sentiment analysis
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Positive"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_create.return_value = mock_response

        analyzer = FeedbackAnalyzer(api_key="fake_key")
        sentiment = analyzer.analyze_sentiment("This is a great app!")
        self.assertEqual(sentiment, "Positive")

    @patch('feedback_analyzer.openai.ChatCompletion.create')
    def test_identify_key_themes(self, mock_create):
        # Mock the API response for theme identification
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Key Themes:\n- Login Issues\n- Billing Problems"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_create.return_value = mock_response

        analyzer = FeedbackAnalyzer(api_key="fake_key")
        themes = analyzer.identify_key_themes(["Can't log in.", "I was double charged."])
        self.assertIn("Login Issues", themes)
        self.assertIn("Billing Problems", themes)

if __name__ == "__main__":
    unittest.main()
