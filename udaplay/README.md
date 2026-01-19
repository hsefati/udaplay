# UdaPlay - AI Game Research Agent Project

## Project Overview
UdaPlay is an AI-powered research agent for the video game industry. This project leverages advanced AI capabilities to help research and answer questions about video games using both local knowledge bases and web searches.

## Project Structure

```
udaplay/
├── lib/                              # Main library modules
│   ├── agents.py                     # AI agent implementations
│   ├── documents.py                  # Document handling utilities
│   ├── evaluation.py                 # Evaluation metrics and tools
│   ├── llm.py                        # Language model integrations
│   ├── loaders.py                    # Data loading utilities
│   ├── long_memory.py                # Long-term memory management
│   ├── messages.py                   # Message handling
│   ├── parsers.py                    # Output parsing utilities
│   ├── rag.py                        # Retrieval-Augmented Generation
│   ├── short_memory.py               # Short-term memory management
│   ├── state_machine.py              # State management
│   ├── tooling.py                    # Tool implementations
│   └── vector_db.py                  # Vector database utilities
├── games/                            # Game data files (JSON format)
├── long_term_memory_db/              # Chroma vector database for long-term memory
├── udaplay_db/                       # Chroma vector database for game data
├── Udaplay_ai_agent.ipynb            # Main AI agent notebook
├── Udaplay_generate_games_vector_db.ipynb  # Vector DB generation notebook
├── pyproject.toml                    # Project configuration and dependencies
├── ruff.toml                         # Ruff linter configuration
└── README.md                         # This file
```

## Requirements

- Python 3.12+
- `uv` package manager

### Dependencies

The project uses the following key dependencies:

- **chromadb** (>=1.4.0) - Vector database for storing and retrieving embeddings
- **openai** (>=2.14.0) - OpenAI API integration for LLM capabilities
- **tavily-python** (>=0.7.17) - Web search capabilities
- **pandas** (>=2.3.3) - Data manipulation and analysis
- **python-dotenv** (>=1.2.1) - Environment variable management
- **pdfplumber** (>=0.11.9) - PDF parsing utilities
- **requests** (>=2.32.5) - HTTP library
- **sqlalchemy** (>=2.0.45) - Database ORM

See `pyproject.toml` for the complete list of dependencies.

## Setup Instructions

### 1. Install `uv` Package Manager

If you haven't already, install `uv`:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or install via package manager:
```bash
# macOS
brew install uv

# Linux (Ubuntu/Debian)
sudo apt install uv
```

### 2. Environment Setup

Create a `.env` file in the project root with the following API keys:

```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
```

### 3. Install Dependencies

Install project dependencies using `uv`:

```bash
# Create a virtual environment and install dependencies
uv sync

# Or install specific dependencies
uv pip install -e .
```

### 4. Running the Project

#### Using Jupyter Notebooks

Start Jupyter:
```bash
# Using uv
uv run jupyter notebook

# Or if jupyter is installed
jupyter notebook
```

> **⚠️ Important:** You must run `Udaplay_generate_games_vector_db.ipynb` **first** to generate the vector database from the game data. This will populate the necessary database files in the `udaplay_db/` directory that the main agent requires.

Then open:
1. **First:** `Udaplay_generate_games_vector_db.ipynb` - Generate vector database from game data
2. **Then:** `Udaplay_ai_agent.ipynb` - Main AI agent implementation

## Development

### Code Quality

This project uses **Ruff** for linting and code quality checks. Configuration is in `ruff.toml`.

Run linting:
```bash
uv run ruff check .
uv run ruff format .
```

