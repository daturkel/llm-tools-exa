# llm-tools-exa

A tool plugin for [LLM](https://llm.datasette.io/) that allows you to search the web using [Exa](https://exa.ai/).

[![PyPI](https://img.shields.io/pypi/v/llm-tools-exa.svg)](https://pypi.org/project/llm-tools-exa/)
[![Changelog](https://img.shields.io/github/v/release/daturkel/llm-tools-exa?include_prereleases&label=changelog)](https://github.com/daturkel/llm-tools-exa/releases)
[![Tests](https://github.com/daturkel/llm-tools-exa/actions/workflows/test.yml/badge.svg)](https://github.com/daturkel/llm-tools-exa/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/daturkel/llm-tools-exa/blob/main/LICENSE)

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/):

```bash
llm install llm-tools-exa
```

## Usage

Create an account at [Exa](https://exa.ai/) and get your API key from [this page](https://dashboard.exa.ai/api-keys). Add it to llm with `llm keys set exa`. 

This plugin provides two tools which can be bundled together or provided separately.

Use `-T Exa` to include both tools, `-T web_search` for web search only, and `-T get_answer` for get answer only.

### web_search
Search the web for high-quality, relevant results with content and highlights:

```bash
llm -m claude-4-sonnet -T web_search "search the web to get today's weather in nyc"
```

### get_answer  
Get a direct answer to a question with optional citations:

```bash
llm -m claude-4-sonnet -T get_answer "What is the capital of France?"
```

You can ask the model to include or omit citations, as desired.

### get_contents
Get the contents of a webpage as markdown:

```bash
llm -m claude-4-sonnet -T get_contents "What's on the homepage of nytimes.com
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-tools-exa
python -m venv venv
source venv/bin/activate
```

Install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
pytest
```

## Dependencies

- [llm](https://llm.datasette.io/): The LLM CLI tool this plugin extends
- [sqlite-utils](https://sqlite-utils.datasette.io/en/stable/): For querying LLM's sqlite databases