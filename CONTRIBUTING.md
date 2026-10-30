# Contributing

## Setup

```sh
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt pytest pytest-cov pre-commit
pre-commit install               # ruff and basic checks on every commit
cp .env.example .env             # the weather key is optional
streamlit run main.py
```

## Before opening a pull request

```sh
pre-commit run --all-files   # ruff lint + format, YAML/TOML checks, private keys, large files
pytest --cov
```

CI runs the same hooks, the tests on Python 3.11, 3.12 and 3.13, and CodeQL. It also reruns
`scripts/evaluate.py` and fails if `reports/evaluation.md` changes, so a change to the ranking
must come with the regenerated report.

Coverage must stay above the `fail_under` value in `pyproject.toml` (currently 95%). Tests must
not call the network: mock `requests` and the translator the way `tests/test_weather.py` and
`tests/test_translation.py` do.

Never commit a real API key. Keys go in `.env`, which is git-ignored.

## Pull requests

- One topic per PR, with a test for the behaviour it adds or fixes.
- Link the issue it closes (`Closes #12`).
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/).
