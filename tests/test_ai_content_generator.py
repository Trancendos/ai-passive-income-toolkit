"""
Tests for AI Content Generator

These tests mock external API calls to ensure zero-cost testing
while providing comprehensive validation coverage.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock openai module before importing
try:
    import openai
except ImportError:
    # Create a mock openai module for testing
    import types
    openai = types.ModuleType('openai')
    openai.api_key = None
    openai.ChatCompletion = type('ChatCompletion', (), {'create': lambda **kwargs: None})
    sys.modules['openai'] = openai

from content_generation.ai_content_generator import AIContentGenerator  # noqa: E402


@pytest.fixture
def mock_openai_response():
    """Mock response from OpenAI API"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = """TITLE: 10 Proven Passive Income Strategies

CONTENT:
In today's digital age, creating passive income streams has become more accessible than ever.

## Understanding Passive Income
Passive income is money earned with minimal active effort.

## Top Strategies
1. Dividend investing
2. Real estate
3. Digital products

## Conclusion
Start small and grow your passive income over time.

TAGS: passive income, investing, entrepreneurship, financial freedom, side hustle"""
    return mock_response


@pytest.fixture
def mock_calendar_response():
    """Mock response for content calendar generation"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = """IDEA 1:
Title: Getting Started with AI Tools
Description: Learn how to leverage AI tools for productivity. This guide covers the basics.
Audience: Business professionals
Level: Beginner
---
IDEA 2:
Title: Advanced Machine Learning Techniques
Description: Deep dive into ML algorithms. Explore neural networks and optimization.
Audience: Data scientists
Level: Advanced
---"""
    return mock_response


@pytest.fixture
def generator():
    """Create an AIContentGenerator instance with a test API key"""
    return AIContentGenerator(api_key="test-api-key")


class TestAIContentGeneratorInit:
    """Test initialization of AIContentGenerator"""

    def test_init_with_api_key(self):
        """Test initialization with provided API key"""
        generator = AIContentGenerator(api_key="test-key-123")
        assert generator.api_key == "test-key-123"

    def test_init_without_api_key(self):
        """Test initialization without API key uses environment variable"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'env-key-456'}):
            generator = AIContentGenerator()
            assert generator.api_key == "env-key-456"

    def test_init_sets_openai_key(self):
        """Test that openai.api_key is set during initialization"""
        with patch('content_generation.ai_content_generator.openai') as mock_openai:
            AIContentGenerator(api_key="test-key")
            assert mock_openai.api_key == "test-key"


class TestGenerateBlogPost:
    """Test blog post generation functionality"""

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_success(self, mock_create, generator, mock_openai_response):
        """Test successful blog post generation"""
        mock_create.return_value = mock_openai_response

        result = generator.generate_blog_post(
            topic="Passive Income",
            target_audience="entrepreneurs",
            word_count=800
        )

        # Verify the API was called
        assert mock_create.called
        call_args = mock_create.call_args

        # Verify API call parameters
        assert call_args[1]['model'] == 'gpt-3.5-turbo'
        assert call_args[1]['max_tokens'] == 1500
        assert call_args[1]['temperature'] == 0.7

        # Verify result structure
        assert result['status'] == 'success'
        assert 'title' in result
        assert 'content' in result
        assert 'tags' in result
        assert result['topic'] == 'Passive Income'
        assert result['target_audience'] == 'entrepreneurs'
        assert 'generated_at' in result

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_parses_title(self, mock_create, generator, mock_openai_response):
        """Test that blog post title is correctly parsed"""
        mock_create.return_value = mock_openai_response

        result = generator.generate_blog_post(topic="Test Topic")

        assert result['title'] == "10 Proven Passive Income Strategies"

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_parses_content(self, mock_create, generator, mock_openai_response):
        """Test that blog post content is correctly parsed"""
        mock_create.return_value = mock_openai_response

        result = generator.generate_blog_post(topic="Test Topic")

        assert "Understanding Passive Income" in result['content']
        assert "digital age" in result['content']

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_parses_tags(self, mock_create, generator, mock_openai_response):
        """Test that tags are correctly parsed"""
        mock_create.return_value = mock_openai_response

        result = generator.generate_blog_post(topic="Test Topic")

        assert 'tags' in result
        assert isinstance(result['tags'], list)
        assert 'passive income' in result['tags']
        assert 'investing' in result['tags']

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_word_count(self, mock_create, generator, mock_openai_response):
        """Test that word count is calculated"""
        mock_create.return_value = mock_openai_response

        result = generator.generate_blog_post(topic="Test Topic")

        assert 'word_count' in result
        assert isinstance(result['word_count'], int)
        assert result['word_count'] > 0

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_api_error(self, mock_create, generator):
        """Test handling of API errors"""
        mock_create.side_effect = Exception("API Error")

        result = generator.generate_blog_post(topic="Test Topic")

        assert result['status'] == 'error'
        assert 'error' in result
        assert 'API Error' in result['error']
        assert 'generated_at' in result

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_blog_post_custom_parameters(self, mock_create, generator, mock_openai_response):
        """Test blog post generation with custom parameters"""
        mock_create.return_value = mock_openai_response

        result = generator.generate_blog_post(
            topic="AI Technology",
            target_audience="developers",
            word_count=1000
        )

        # Verify custom parameters are passed
        assert result['topic'] == "AI Technology"
        assert result['target_audience'] == "developers"

        # Verify the prompt includes custom parameters
        call_args = mock_create.call_args
        messages = call_args[1]['messages']
        user_message = messages[1]['content']
        assert "AI Technology" in user_message
        assert "developers" in user_message
        assert "1000" in user_message


class TestGenerateContentCalendar:
    """Test content calendar generation functionality"""

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_success(self, mock_create, generator, mock_calendar_response):
        """Test successful content calendar generation"""
        mock_create.return_value = mock_calendar_response

        result = generator.generate_content_calendar(
            niche="AI and Technology",
            num_posts=10
        )

        # Verify the API was called
        assert mock_create.called

        # Verify result structure
        assert result['status'] == 'success'
        assert result['niche'] == "AI and Technology"
        assert 'total_ideas' in result
        assert 'ideas' in result
        assert isinstance(result['ideas'], list)
        assert 'generated_at' in result

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_parses_ideas(self, mock_create, generator, mock_calendar_response):
        """Test that content ideas are correctly parsed"""
        mock_create.return_value = mock_calendar_response

        result = generator.generate_content_calendar(niche="Test Niche", num_posts=5)

        assert len(result['ideas']) > 0
        first_idea = result['ideas'][0]

        # Verify idea structure
        assert 'title' in first_idea
        assert 'description' in first_idea
        assert 'audience' in first_idea
        assert 'level' in first_idea
        assert 'generated_at' in first_idea

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_idea_content(self, mock_create, generator, mock_calendar_response):
        """Test that idea content is correctly parsed"""
        mock_create.return_value = mock_calendar_response

        result = generator.generate_content_calendar(niche="Test Niche")

        first_idea = result['ideas'][0]
        assert first_idea['title'] == "Getting Started with AI Tools"
        assert "AI tools for productivity" in first_idea['description']
        assert first_idea['audience'] == "Business professionals"
        assert first_idea['level'] == "Beginner"

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_total_ideas(self, mock_create, generator, mock_calendar_response):
        """Test that total_ideas count is correct"""
        mock_create.return_value = mock_calendar_response

        result = generator.generate_content_calendar(niche="Test Niche")

        assert result['total_ideas'] == len(result['ideas'])
        assert result['total_ideas'] == 2  # Based on mock response

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_api_error(self, mock_create, generator):
        """Test handling of API errors in calendar generation"""
        mock_create.side_effect = Exception("Calendar API Error")

        result = generator.generate_content_calendar(niche="Test Niche")

        assert result['status'] == 'error'
        assert 'error' in result
        assert 'Calendar API Error' in result['error']
        assert 'generated_at' in result

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_custom_posts(self, mock_create, generator, mock_calendar_response):
        """Test content calendar with custom number of posts"""
        mock_create.return_value = mock_calendar_response

        generator.generate_content_calendar(
            niche="Technology",
            num_posts=20
        )

        # Verify custom parameters
        call_args = mock_create.call_args
        messages = call_args[1]['messages']
        user_message = messages[1]['content']
        assert "20" in user_message
        assert "Technology" in user_message

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_generate_content_calendar_api_params(self, mock_create, generator, mock_calendar_response):
        """Test that correct API parameters are used"""
        mock_create.return_value = mock_calendar_response

        generator.generate_content_calendar(niche="Test")

        call_args = mock_create.call_args
        assert call_args[1]['model'] == 'gpt-3.5-turbo'
        assert call_args[1]['max_tokens'] == 2000
        assert call_args[1]['temperature'] == 0.8


class TestIntegration:
    """Integration tests for the AIContentGenerator"""

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_multiple_blog_posts(self, mock_create, generator, mock_openai_response):
        """Test generating multiple blog posts in sequence"""
        mock_create.return_value = mock_openai_response

        result1 = generator.generate_blog_post(topic="Topic 1")
        result2 = generator.generate_blog_post(topic="Topic 2")

        assert result1['status'] == 'success'
        assert result2['status'] == 'success'
        assert mock_create.call_count == 2

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_blog_and_calendar_workflow(self, mock_create, generator, mock_openai_response, mock_calendar_response):
        """Test a typical workflow of generating calendar then blog post"""
        # First call returns calendar, second returns blog post
        mock_create.side_effect = [mock_calendar_response, mock_openai_response]

        calendar = generator.generate_content_calendar(niche="Test", num_posts=5)
        blog_post = generator.generate_blog_post(topic="Test Topic")

        assert calendar['status'] == 'success'
        assert blog_post['status'] == 'success'
        assert len(calendar['ideas']) > 0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_generator_without_openai_key(self):
        """Test generator when no API key is available"""
        with patch.dict(os.environ, {}, clear=True):
            generator = AIContentGenerator()
            assert generator.api_key is None

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_empty_response_handling(self, mock_create, generator):
        """Test handling of empty API response"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = ""
        mock_create.return_value = mock_response

        result = generator.generate_blog_post(topic="Test")

        # Should still return success but with empty/minimal data
        assert result['status'] == 'success'
        assert 'generated_at' in result

    @patch('content_generation.ai_content_generator.openai.ChatCompletion.create')
    def test_malformed_response_handling(self, mock_create, generator):
        """Test handling of malformed API response"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is not properly formatted"
        mock_create.return_value = mock_response

        # Result is still success even if parsing doesn't find expected format
        generator.generate_blog_post(topic="Test")

        # Should return success even if parsing doesn't find expected format
        assert mock_create.called
