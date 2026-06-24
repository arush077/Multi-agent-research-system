import pytest
from pipeline import run_research_pipeline


def test_happy_path():
    # Test the research pipeline with a valid topic.
    topic = 'Test Topic'
    result = run_research_pipeline(topic)
    assert 'search_results' in result
    assert 'scraped_content' in result
    assert 'report' in result
    assert 'feedback' in result


def test_edge_case_empty_topic():
    # Test the research pipeline with an empty topic.
    topic = ''
    with pytest.raises(Exception):
        run_research_pipeline(topic)


def test_edge_case_none_topic():
    # Test the research pipeline with a None topic.
    topic = None
    with pytest.raises(Exception):
        run_research_pipeline(topic)


def test_regression_existing_functionality():
    # Test that the existing functionality of the research pipeline still works.
    topic = 'Test Topic'
    result = run_research_pipeline(topic)
    assert result['search_results'] is not None
    assert result['scraped_content'] is not None
    assert result['report'] is not None
    assert result['feedback'] is not None