# PyFind v1.0

PyFind is a fast, Python-powered file discovery and content–search utility for Unix terminals. It combines glob or regex name matching, optional in‐file regex grepping, parallel directory traversal, colored output, and an interactive fuzzy-search TUI with live preview—all in a single script.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Command-Line Options](#command-line-options)  
- [Interactive Mode](#interactive-mode)  
- [Examples](#examples)  
- [Configuration](#configuration)  
- [Contributing](#contributing)  
- [License](#license)  
- [Author](#author)  

---

## Overview

PyFind walks your file tree in parallel, skipping unwanted directories (for example `.git`, `venv`), and matches file names by glob‐patterns (`*.py`) or full Python regex. Optionally, it will search inside files for regex patterns. Results are colorized for readability. An optional interactive mode powered by PromptToolkit offers fuzzy filtering of file paths plus a preview of matching lines.

---

## Features

- Name‐based search using glob or regex  
- Content‐search with full regex support  
- Parallel filesystem traversal with `ThreadPoolExecutor`  
- Configurable directory exclusions (default: `.git`, `.venv`)  
- Colorized output via Colorama  
- Interactive fuzzy‐search TUI with live preview (requires PromptToolkit)  
- Single‐file deployment—no complex install or external index  

---

## Prerequisites

- **Python** 3.6 or newer  
- Unix‐style terminal (Linux, macOS, WSL)  
- **Dependencies** (install via `pip`):  
  - `colorama`  
  - `regex`  
  - *(optional for TUI)* `prompt_toolkit`  

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/bocaletto-luca/PyFind.git
cd PyFind
pip install colorama regex prompt_toolkit
chmod +x pyfind.py
```

Or grab the single script directly:

```bash
curl -Lo pyfind.py \
  https://raw.githubusercontent.com/bocaletto-luca/PyFind/main/pyfind.py
chmod +x pyfind.py
```

---

## Usage

```bash
./pyfind.py [pattern] [options]
```

- **pattern**: glob (e.g. `*.md`) or Python regex (e.g. `^test_.*\.py$`)  
- **-c, --content**: regex to match inside files  
- **-r, --root**: directory to search (default: `.`)  
- **--ignore**: space-separated list of dirs to skip  
- **-i, --interactive**: launch fuzzy TUI mode  

---

## Command-Line Options

| Option                 | Description                                                  |
|------------------------|--------------------------------------------------------------|
| `pattern`              | Required glob or regex for file names                       |
| `-c, --content <regex>`| Search inside file contents using this Python regex         |
| `-r, --root <path>`    | Root directory to scan (default: current directory)         |
| `--ignore <dirs>`      | Directories to skip (default: `.git`, `.venv`)               |
| `-i, --interactive`    | Start fuzzy‐search TUI (requires `prompt_toolkit`)          |

---

## Interactive Mode

Launch PyFind in TUI mode for fuzzy filtering:

```bash
./pyfind.py "*.py" -i
```

- **Fuzzy completion** over all matching file paths  
- **Live preview** of up to 10 matching lines per file  
- Up/Down or typing to refine, Ctrl+C to exit  

---

## Examples

```bash
# 1) Find all .py files under src/, skip .git and venv
./pyfind.py "*.py" --root src/ --ignore .git venv

# 2) Search for “TODO” inside all JavaScript files
./pyfind.py "*.js" -c "TODO"

# 3) Regex match filenames starting with “test_”
./pyfind.py "^test_.*\.py$"

# 4) Interactive fuzzy search for “config” in any filename
./pyfind.py "config" -i
```

---

## Configuration

PyFind has no external config by default. To customize ignored directories or default root, you can create a small wrapper or alias. For example:

```bash
alias pyfind='~/tools/pyfind.py --ignore .git build --root ~/myproject'
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/foo`)  
3. Commit your changes with clear messages  
4. Open a pull request describing your improvements  

Please follow [PEP 8](https://peps.python.org/pep-0008/) style and include examples or tests for new features.

---

## License

PyFind is released under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Author

**Luca Bocaletto**  
- 🔗 GitHub: [bocaletto-luca](https://github.com/bocaletto-luca)  
- 🌐 Website: https://bocaletto-luca.github.io  

---
