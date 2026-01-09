# replacetext

**Bulk text replacement in files using dictionary mappings.**

[![PyPI version](https://badge.fury.io/py/replacetext.svg)](https://badge.fury.io/py/replacetext)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Replace text across multiple files using find/replace dictionaries. Supports bidirectional replacement (keys-to-values or values-to-keys).

## Installation

```bash
pip install replacetext
```

## Quick Start

1. Create a config file (`config.json`):

```json
{
  "dictionaries": {
    "example": {
      "old_text": "new_text",
      "foo": "bar"
    }
  },
  "ignore_extensions": [".exe", ".bin"],
  "ignore_directories": ["node_modules", ".git"],
  "ignore_file_prefixes": [".", "_"]
}
```

2. Run:

```bash
replacetext -f ./my_folder -d 1
```

## Usage

```bash
# Interactive mode
replacetext

# With options
replacetext --folder ./src --direction 1 --config my_config.json

# Dry run (preview changes)
replacetext -f ./src -d 1 --dry-run

# Reverse direction (values-to-keys)
replacetext -f ./src -d 2
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--folder` | `-f` | Folder to process |
| `--direction` | `-d` | 1 = keys-to-values, 2 = values-to-keys |
| `--config` | `-c` | Path to config file (default: config.json) |
| `--dict-name` | `-n` | Dictionary name (auto-selects if only one) |
| `--dry-run` | | Preview changes without modifying files |

## Config Format

```json
{
  "dictionaries": {
    "my_replacements": {
      "find_this": "replace_with_this",
      "old": "new"
    }
  },
  "ignore_extensions": [".exe", ".dll"],
  "ignore_directories": ["node_modules", "venv"],
  "ignore_file_prefixes": [".", "_"]
}
```

## License

GPL v3
