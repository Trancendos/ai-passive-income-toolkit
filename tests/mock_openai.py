# Mock openai module for testing
"""
This module provides mock implementations of OpenAI API for testing purposes.
"""


class ChatCompletion:
    @staticmethod
    def create(**kwargs):
        raise NotImplementedError("OpenAI API should be mocked in tests")


api_key = None
