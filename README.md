# CienaLLM

CienaLLM is a modular Python framework for **schema-guided Generative Information Extraction (GenIE)** from climate-related news using open-weight Large Language Models (LLMs). It enables configurable prompts, multi-step extraction pipelines (summarization, self-criticism, chain-of-thought), and structured JSON outputs.

The framework was developed and evaluated in *Vela-Tambo et al. (2025, to be published)*, focusing on extracting drought impacts from Spanish news articles. Its modular design makes it easily extensible to other hazards, domains, and languages.

---

## Features

* Schema-guided extraction with configurable prompts and schemas
* Multi-step pipelines: summarization, chain-of-thought, self-criticism
* Structured output parsing and validation with [Pydantic](https://docs.pydantic.dev/latest/)
* LLM orchestration through [LangChain](https://www.langchain.com/) and [Ollama](https://ollama.com/)
* Modular design with reproducible experiments via YAML configuration
* Support for both local inference and cloud-based LLMs

---

## Project Structure

```txt
.
├── README.md                       # This file
├── LICENSE                         # MIT license text
├── pyproject.toml                  # Poetry configuration file
├── poetry.lock
├── src                             # Source code
│   └── ciena_llm
│       ├── article                 # Article processing and handling
│       ├── llm                     # LLM interaction
│       ├── chain                   # Each LLM step definition
│       ├── extraction_schema       # Extraction schema definition
│       ├── prompt                  # Prompt definitions and management
│       ├── output                  # Output handling and formatting
│       ├── config                  # Configuration handling
│       │   └── config.yaml         # Default configuration file
│       └── __init__.py
├── experiments                     # Scripts for experiment execution
└── tests                           # Scripts for testing
    ├── common
    ├── test_event.py               # Test script for event relevance extraction
    ├── test_impact.py              # Test script for impact extraction
    ├── test_location.py            # Test script for location extraction
    └── test_hail_event.py          # Test script for hail event extraction
```

---

## Installation

Ensure you have Python 3.10+ installed. Install dependencies with [Poetry](https://python-poetry.org/):

```bash
poetry install
```

Alternatively, you can install dependencies using another method (e.g., `pip`) if you prefer.

---

## Usage

1. **Configuration**:
   Create a script that uses the `ciena_llm` package.
   Example scripts can be found in the `tests` directory.

   You can either:

   * Set up your configuration in `config.yaml`, or

   * Pass a config file directly in your script.

2. **Execution**:
   Run your script with Poetry:

   ```bash
   poetry run python your_script.py
   ```

---

## Datasets

This repository does **not** include datasets.
The experiments described in the accompanying paper used re-annotated drought-related Spanish news datasets. These will be released separately upon publication.

You can run the framework on your own corpora of news articles formatted according to the [NewsArticle schema](https://schema.org/NewsArticle).

---

## Citation

If you use this framework in your research, please cite:

```bibtex
@misc{vela2025cienallm,
  author = {Javier Vela-Tambo and Jorge Gracia and Fernando Domínguez-Castro},
  title = {CienaLLM: Generative Climate-Impact Extraction from News Articles with Autoregressive LLMs},
  year = {2025},
  note = {To be published}
}
```

---

## Contributing

Contributions are welcome!
Please open an issue or pull request if you’d like to improve the code, add features, or report bugs.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
