# Contributing to textswap

Thanks for your interest in contributing to textswap!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/cainky/ReplaceText.git
cd ReplaceText
```

2. Install in development mode:
```bash
pip install -e ".[dev]"
```

This installs the package along with development dependencies (pytest, ruff).

## Running Tests

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

## Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

Check linting:
```bash
ruff check .
```

Check formatting:
```bash
ruff format --check .
```

Auto-fix issues:
```bash
ruff check --fix .
ruff format .
```

## Making Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Add tests for new functionality
4. Run the test suite to ensure nothing is broken
5. Run linting/formatting checks
6. Submit a pull request

## Pull Request Guidelines

- Keep PRs focused on a single change
- Include tests for new features or bug fixes
- Update documentation if needed
- Follow existing code style

## Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant config file (redacted if sensitive)

## Questions?

Open an issue for discussion before starting work on major changes.
