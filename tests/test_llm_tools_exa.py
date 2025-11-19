from unittest.mock import Mock, patch

import pytest

from llm_tools_exa import ExaTools


@pytest.fixture
def exa_tools():
    """Create ExaTools instance for testing."""
    return ExaTools()


@pytest.fixture
def mock_exa_result():
    """Mock Exa search result object."""
    result = Mock()
    result.title = "Test Title"
    result.author = "Test Author"
    result.url = "https://example.com"
    result.published_date = "2024-01-01"
    result.text = "This is the full text content of the result."
    return result


@pytest.fixture
def mock_exa_response(mock_exa_result):
    """Mock Exa API response."""
    response = Mock()
    response.results = [mock_exa_result]
    return response


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_basic(mock_get_key, mock_exa_class, mock_exa_response, exa_tools):
    """Test basic web search functionality."""
    # Setup mocks
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.search_and_contents.return_value = mock_exa_response
    mock_exa_class.return_value = mock_exa_instance

    # Call function
    result = exa_tools.web_search("test query")

    # Verify API calls
    mock_get_key.assert_called_once_with(
        explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
    )
    mock_exa_class.assert_called_once_with("test_api_key")
    mock_exa_instance.search_and_contents.assert_called_once_with(
        query="test query",
        num_results=3,
        category=None,
        type="auto",
        include_domains=None,
        text=True,
    )

    # Verify output format
    assert "Title: Test Title" in result
    assert "Author: Test Author" in result
    assert "URL: https://example.com" in result
    assert "Published: 2024-01-01" in result
    assert "Text: This is the full text content of the result." in result
    assert "---------" in result


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_with_parameters(
    mock_get_key, mock_exa_class, mock_exa_response, exa_tools
):
    """Test web search with custom parameters."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.search_and_contents.return_value = mock_exa_response
    mock_exa_class.return_value = mock_exa_instance

    # Call with custom parameters
    exa_tools.web_search(
        query="python tutorials",
        num_results=5,
        category="research paper",
        include_domains=["github.com", "stackoverflow.com"],
    )

    # Verify parameters passed correctly
    mock_exa_instance.search_and_contents.assert_called_once_with(
        query="python tutorials",
        num_results=5,
        category="research paper",
        type="auto",
        include_domains=["github.com", "stackoverflow.com"],
        text=True,
    )


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_multiple_results(mock_get_key, mock_exa_class, exa_tools):
    """Test web search with multiple results."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    # Create multiple mock results
    result1 = Mock()
    result1.title = "First Result"
    result1.author = "Author 1"
    result1.url = "https://example1.com"
    result1.published_date = "2024-01-01"
    result1.text = "Text 1"

    result2 = Mock()
    result2.title = "Second Result"
    result2.author = "Author 2"
    result2.url = "https://example2.com"
    result2.published_date = "2024-01-02"
    result2.text = "Text 2"

    mock_response = Mock()
    mock_response.results = [result1, result2]
    mock_exa_instance.search_and_contents.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = exa_tools.web_search("test query")

    # Verify both results are in output
    assert "First Result" in result
    assert "Second Result" in result
    assert "https://example1.com" in result
    assert "https://example2.com" in result
    assert result.count("---------") == 2  # Separator appears for each result


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_empty_results(mock_get_key, mock_exa_class, exa_tools):
    """Test web search with no results."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    mock_response = Mock()
    mock_response.results = []
    mock_exa_instance.search_and_contents.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = exa_tools.web_search("nonexistent query")

    # Should return empty string when no results
    assert result == ""


@pytest.mark.parametrize(
    "category",
    [
        "company",
        "research paper",
        "news",
        "pdf",
        "github",
        "tweet",
        "personal site",
        "linkedin profile",
        "financial report",
    ],
)
@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_web_search_valid_categories(
    mock_get_key, mock_exa_class, mock_exa_response, category, exa_tools
):
    """Test web search with all valid category values."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.search_and_contents.return_value = mock_exa_response
    mock_exa_class.return_value = mock_exa_instance

    exa_tools.web_search("test", category=category)

    mock_exa_instance.search_and_contents.assert_called_once_with(
        query="test",
        num_results=3,
        category=category,
        type="auto",
        include_domains=None,
        text=True,
    )


@pytest.fixture
def mock_answer_citation():
    """Mock Exa answer citation object."""
    citation = Mock()
    citation.title = "Citation Title"
    citation.url = "https://citation.com"
    citation.published_date = "2024-01-01"
    return citation


@pytest.fixture
def mock_answer_response(mock_answer_citation):
    """Mock Exa answer API response."""
    response = Mock()
    response.answer = "This is the answer to your question."
    response.citations = [mock_answer_citation]
    return response


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_answer_basic(
    mock_get_key, mock_exa_class, mock_answer_response, exa_tools
):
    """Test basic get_answer functionality."""
    # Setup mocks
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.answer.return_value = mock_answer_response
    mock_exa_class.return_value = mock_exa_instance

    # Call function
    result = exa_tools.get_answer("What is Python?")

    # Verify API calls
    mock_get_key.assert_called_once_with(
        explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
    )
    mock_exa_class.assert_called_once_with("test_api_key")
    mock_exa_instance.answer.assert_called_once_with(
        query="What is Python?", stream=False, text=False
    )

    # Verify output format
    assert "This is the answer to your question." in result
    assert "Citation: Citation Title" in result
    assert "URL: https://citation.com" in result
    assert "Published: 2024-01-01" in result


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_answer_multiple_citations(mock_get_key, mock_exa_class, exa_tools):
    """Test get_answer with multiple citations."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    # Create multiple mock citations
    citation1 = Mock()
    citation1.title = "First Citation"
    citation1.url = "https://first.com"
    citation1.published_date = "2024-01-01"

    citation2 = Mock()
    citation2.title = "Second Citation"
    citation2.url = "https://second.com"
    citation2.published_date = "2024-01-02"

    mock_response = Mock()
    mock_response.answer = "Comprehensive answer with multiple sources."
    mock_response.citations = [citation1, citation2]

    mock_exa_instance.answer.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = exa_tools.get_answer("Complex question")

    # Verify both citations are in output
    assert "Comprehensive answer with multiple sources." in result
    assert "First Citation" in result
    assert "Second Citation" in result
    assert "https://first.com" in result
    assert "https://second.com" in result


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_answer_no_citations(mock_get_key, mock_exa_class, exa_tools):
    """Test get_answer with no citations."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    mock_response = Mock()
    mock_response.answer = "Answer without citations."
    mock_response.citations = []

    mock_exa_instance.answer.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = exa_tools.get_answer("Simple question")

    # Should only contain the answer
    assert result == "Answer without citations."


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_answer_citations_false(
    mock_get_key, mock_exa_class, mock_answer_response, exa_tools
):
    """Test get_answer with citations=False."""
    # Setup mocks
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.answer.return_value = mock_answer_response
    mock_exa_class.return_value = mock_exa_instance

    # Call function with citations=False
    result = exa_tools.get_answer("What is Python?", citations=False)

    # Verify API calls
    mock_exa_instance.answer.assert_called_once_with(
        query="What is Python?", stream=False, text=False
    )

    # Verify output contains only answer, no citations
    assert result == "This is the answer to your question."
    assert "Citation:" not in result
    assert "URL:" not in result
    assert "Published:" not in result


@pytest.fixture
def mock_contents_response():
    """Mock Exa get_contents API response."""
    response = Mock()
    response.context = (
        "# Example Article\n\nThis is the markdown content of the webpage."
    )
    return response


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_contents_basic(
    mock_get_key, mock_exa_class, mock_contents_response, exa_tools
):
    """Test basic get_contents functionality."""
    # Setup mocks
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()
    mock_exa_instance.get_contents.return_value = mock_contents_response
    mock_exa_class.return_value = mock_exa_instance

    # Call function
    result = exa_tools.get_contents("https://example.com")

    # Verify API calls
    mock_get_key.assert_called_once_with(
        explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
    )
    mock_exa_class.assert_called_once_with("test_api_key")
    mock_exa_instance.get_contents.assert_called_once_with(
        urls=["https://example.com"], text=True, context=True
    )

    # Verify output
    assert result == "# Example Article\n\nThis is the markdown content of the webpage."


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_contents_different_url(mock_get_key, mock_exa_class, exa_tools):
    """Test get_contents with a different URL."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    mock_response = Mock()
    mock_response.context = "Different webpage content here."
    mock_exa_instance.get_contents.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = exa_tools.get_contents("https://different-site.com/article")

    # Verify correct URL was passed
    mock_exa_instance.get_contents.assert_called_once_with(
        urls=["https://different-site.com/article"], text=True, context=True
    )
    assert result == "Different webpage content here."


@patch("llm_tools_exa.Exa")
@patch("llm_tools_exa.llm.get_key")
def test_get_contents_empty_content(mock_get_key, mock_exa_class, exa_tools):
    """Test get_contents with empty content."""
    mock_get_key.return_value = "test_api_key"
    mock_exa_instance = Mock()

    mock_response = Mock()
    mock_response.context = ""
    mock_exa_instance.get_contents.return_value = mock_response
    mock_exa_class.return_value = mock_exa_instance

    result = exa_tools.get_contents("https://empty-page.com")

    assert result == ""
