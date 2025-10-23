# Contributing to CIS Benchmark Compliance Checker

Thank you for your interest in contributing! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)

### Suggesting Features

1. Check if the feature has been suggested
2. Create an issue describing:
   - The problem it solves
   - Proposed solution
   - Alternative solutions considered

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Run code quality checks (`black src/`, `flake8 src/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to your fork (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Add type hints to functions
- Write descriptive docstrings
- Maximum line length: 88 characters

## Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Run full test suite before submitting PR

## Documentation

- Update README.md if adding features
- Add docstrings to new functions/classes
- Update API documentation if needed

## Code of Conduct

Please be respectful and professional in all interactions.
