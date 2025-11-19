from typing import Literal, Optional, cast

import llm
from exa_py import Exa
from exa_py.api import AnswerResponse, SearchResponse


class ExaTools(llm.Toolbox):
    name: str = "Exa Tools"

    def web_search(
        self,
        query: str,
        num_results: int = 3,
        category: Optional[
            Literal[
                "company",
                "research paper",
                "news",
                "pdf",
                "github",
                "tweet",
                "personal site",
                "linkedin profile",
                "financial report",
            ]
        ] = None,
        include_domains: Optional[list[str]] = None,
    ):
        """Search the web using Exa API for high-quality, relevant results.

        Args:
            query: The search query string to find relevant content.
            num_results: Number of search results to return (default: 3).
            category: Optional content category to filter results by specific type.
            include_domains: Optional list of domains to limit search results to.
        """
        exa_key = llm.get_key(
            explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
        )
        exa = Exa(exa_key)
        results = exa.search_and_contents(
            query=query,
            num_results=num_results,
            category=category,
            type="auto",
            include_domains=include_domains,
            text=True,
        ).results
        output = []
        for result in results:
            output.append(f"Title: {result.title}")
            output.append(f"Author: {result.author}")
            output.append(f"URL: {result.url}")
            output.append(f"Published: {result.published_date}")
            output.append(f"Text: {result.text}")
            output.append("---------\n")
        return "\n".join(output)

    def get_answer(self, query: str, citations: bool = True):
        """Get a direct answer to a question using Exa API with optional citations.

        Args:
            query: The question to get an answer for.
            citations: Whether to include citations in the response (default: True).
        """
        exa_key = llm.get_key(
            explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
        )
        exa = Exa(exa_key)
        answer = cast(AnswerResponse, exa.answer(query=query, stream=False, text=False))
        output = [str(answer.answer)]
        if citations:
            for citation in answer.citations:
                output.append(f"Citation: {citation.title}")
                output.append(f"URL: {citation.url}")
                output.append(f"Published: {citation.published_date}")
        return "\n".join(output)

    def get_contents(self, url: str) -> str:
        """Get the contents of a webpage in text format.

        Args:
            url: The URL to summarize.

        Returns:
            The contents of the website as markdown.
        """
        exa_key = llm.get_key(
            explicit_key="exa", key_alias="exa", env_var="EXA_API_KEY"
        )
        exa = Exa(exa_key)
        result = cast(
            SearchResponse,
            exa.get_contents(urls=[url], text=True, context=True),  # type: ignore
        )
        return result.context  # type: ignore


@llm.hookimpl
def register_tools(register):
    exa_tools = ExaTools()
    register(exa_tools.web_search, "web_search")
    register(exa_tools.get_answer, "get_answer")
    register(exa_tools.get_contents, "get_contents")
    register(ExaTools, "Exa")
