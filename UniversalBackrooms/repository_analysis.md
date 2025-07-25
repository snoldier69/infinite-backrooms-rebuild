# UniversalBackrooms Repository Analysis

This document outlines the purpose and functionality of key files within the `UniversalBackrooms` GitHub repository.

## `backrooms.py`
This is the core Python script responsible for managing and executing AI model conversations. Its main functionalities include:
- **Model Orchestration**: Selects and integrates various AI models (e.g., Claude, GPT-4o, O1) for conversational roles.
- **Template Loading**: Loads conversation structures and initial prompts from `.jsonl` files located in the `templates/` directory.
- **Conversation Management**: Manages the flow of conversation turns between selected models, including handling system prompts and context transitions.
- **Logging**: Records generated conversations into text files within the `BackroomsLogs/` directory, including model names, template used, and a timestamp.
- **CLI Integration**: Supports interaction with a command-line interface (CLI) for specific conversation templates.
- **API Key Management**: Utilizes API keys loaded from environment variables (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`).

## `templates/`
This directory contains `.jsonl` files, each defining a specific conversation template. These templates are crucial for shaping the initial setup and context of a conversation. Each `.jsonl` file typically contains:
- **System Prompts**: Initial instructions or roles given to the AI models.
- **Context**: Pre-defined conversational turns or messages that set the scene for the AI models.
- **Model Configuration**: Specifies which models are intended for which roles within the conversation.

Examples of templates include `cli.jsonl`, `student.jsonl`, `science.jsonl`, `fugue.jsonl`, `gallery.jsonl`, and `ethics.jsonl`.

## `BackroomsLogs/`
This directory serves as the storage location for all generated conversation logs. Each log file is named using a convention that includes the models involved, the template used, and a timestamp (e.g., `opus_opus_cli_20241018_225330.txt`). These logs capture the full dialogue between the AI models, providing a record of the generated conversations.

## `.env.example`
This file provides an example of the environment variables that need to be set for the `backrooms.py` script to function correctly. It primarily lists placeholders for API keys required to access the AI models:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `WORLD_INTERFACE_KEY` (for CLI integration)

## `requirements.txt`
This file lists all the Python dependencies required to run the `backrooms.py` script. It ensures that the necessary libraries (e.g., `anthropic`, `openai`, `python-dotenv`, `requests`) are installed in the environment, allowing the script to execute without missing modules.

