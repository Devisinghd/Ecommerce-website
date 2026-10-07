# Contributing to Ecommerce Website

Thanks for your interest in contributing to this project. This repository is a Django-based e-commerce backend and we welcome thoughtful contributions from beginners and experienced developers alike.

## Ways to contribute

You can help by:

- fixing bugs
- improving documentation
- adding tests
- improving frontend or API usability
- proposing product features
- creating beginner-friendly tasks for other contributors

## Before you start

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your work
4. Read the project README and setup instructions
5. Make sure your changes are relevant and well-scoped

## Local setup

```bash
git clone https://github.com/Devisinghd/Ecommerce-website.git
cd Ecommerce-website
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Coding standards

- Follow PEP 8 for Python code
- Keep functions and classes focused and readable
- Write tests for bug fixes and new features when possible
- Prefer clear naming over clever shortcuts
- Keep pull requests small and easy to review

## Pull request guidelines

- Open a pull request only for a focused change
- Include a clear title and summary of your work
- Mention the related issue or feature request
- Add screenshots or examples when UI or API behavior changes
- Keep the commit history clean and readable

## Good first issues

Look for issues labeled `good first issue` in the repository. If you want to create a beginner-friendly task, see the issue ideas in `GOOD_FIRST_ISSUES.md`.

## Reporting bugs

When reporting a bug, include:

- a short description
- reproduction steps
- expected behavior
- actual behavior
- screenshots or terminal output if possible

## Respect and collaboration

We expect contributors to be respectful, constructive, and patient. Disagreements should be handled in a professional and solution-focused manner.

## Questions?

If you are unsure where to start, open a discussion or ask in the project issue tracker. We are happy to help new contributors begin.
