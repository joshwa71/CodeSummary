# Codebase Summarizer

## Overview

This repository contains a Python script called `summariser.py` that automatically summarizes each file in a given codebase. It then uses these summaries to generate a `README.md` file. The script leverages the GPT-4 API for generating these summaries and the readme content.

## Usage

### Prerequisites

- Python 3.x
- `requests` library
- OpenAI API Key

### Command-Line Arguments

The script takes a mandatory command-line argument `--api_key`, which is the OpenAI API key used for making calls to the GPT-4 API.

#### Example:

```bash
python summariser.py --api_key YOUR_OPENAI_API_KEY