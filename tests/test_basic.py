"""
Basic test to ensure the test infrastructure works.
This test will pass and allow the CI workflow to complete successfully.
"""


def test_basic_import():
    """Test that Python imports work correctly."""
    import sys
    assert sys.version_info >= (3, 9), "Python version should be 3.9 or higher"


def test_requirements_file_exists():
    """Test that requirements.txt exists."""
    import os
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    requirements_path = os.path.join(repo_root, 'requirements.txt')
    assert os.path.exists(requirements_path), "requirements.txt should exist in repo root"


def test_content_generation_module_exists():
    """Test that the content-generation module exists."""
    import os
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_gen_path = os.path.join(repo_root, 'content-generation')
    assert os.path.exists(content_gen_path), "content-generation directory should exist"
