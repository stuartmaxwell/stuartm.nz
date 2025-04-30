# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

- Run tests: `just test`
- Run single test: `just test tests/path_to_test.py::TestClass::test_name`

## Code Style Guidelines

- **Python**:
  - Use 4-space indentation
  - Max line length: 120 characters
  - Follow Google docstring style
  - Use type hints for function parameters and returns
  - Use ruff for linting and formatting
- **Templates**:
  - Use 2-space indentation
  - Follow Django template conventions
- **JavaScript/CSS**:
  - Use 2-space indentation
  - Format with Prettier

## Naming Conventions

- Django apps: snake_case
- Python: snake_case for variables/functions, PascalCase for classes
- Template files: snake_case.html
- JavaScript: camelCase for variables/functions
- Prefer descriptive names over abbreviations

## Error Handling

- Use Django's built-in error handling where appropriate
- In Python, use try/except blocks with specific exceptions
- Add meaningful error messages for users
