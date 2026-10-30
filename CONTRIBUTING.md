# Contributing

## Setup

```sh
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt pytest pytest-cov ruff
cp .env.example .env             # the weather key is optional
streamlit run main.py
```

## Before opening a pull request

```sh
ruff check .
ruff format --check .
pytest --cov
```

CI runs the same commands on Python 3.11, 3.12 and 3.13, and runs CodeQL. Coverage must stay
above the `fail_under` value in `pyproject.toml`. Tests must not call the network: mock the
OpenWeatherMap and translation calls instead.

Never commit a real API key. Keys go in `.env`, which is git-ignored.

## Pull requests

- One topic per PR, with a test for the behaviour it adds or fixes.
- Link the issue it closes (`Closes #12`).
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/).
