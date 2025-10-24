import unittest
from unittest.mock import patch, MagicMock
from ai_content_generator import AIContentGenerator

class TestAIContentGenerator(unittest.TestCase):
    @patch('ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_word_count(self, mock_create):
        # Mock the API response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "TITLE: Test Title\nCONTENT:\nThis is the body of the test blog post.\nTAGS: test, blog, post"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_create.return_value = mock_response

        generator = AIContentGenerator(api_key="fake_key")

        # Request a blog post
        blog_post = generator.generate_blog_post(topic="Test Topic", word_count=20)

        # The mock content has 2 words in the title and 8 words in the body, plus one for the newline.
        # The old logic would calculate the word count as 8 (body only).
        # The new logic calculates the word count as 11 (title + body + newline).

        # This assertion will fail with the old logic and pass with the new logic.
        self.assertEqual(blog_post["word_count"], 11, f"Word count is {blog_post['word_count']}, expected 11")

if __name__ == "__main__":
    unittest.main()
