# AGENTS.md for `python-rabe-cridlib`

> This document is intended for automated, agentic helpers and human maintainers who
> want to understand how to work with the repository in the **agentic age**.

## 📁 Repository overview

```
pyproject.toml
ruff.toml
mkdocs.yaml
.
├── cridlib/           # Python package
│   ├── __init__.py   # public API: get, parse, CRIDError
│   ├── get.py        # get() – generate a CRID for a given timestamp
│   ├── lib.py        # CRID class, error hierarchy, canonicalize_show()
│   ├── parse.py      # parse() – parse an existing CRID string
│   ├── util.py       # get_session() – requests Session with retry/backoff
│   └── strategy/     # data-source strategies
│       ├── now.py    # current show via songticker.rabe.ch
│       ├── past.py   # past show via archiv.rabe.ch (RAAR)
│       └── future.py # future show via LibreTime API (internal)
├── docs/             # MkDocs documentation helpers
└── tests/            # pytest-based unit tests
    ├── conftest.py
    ├── strategy/
    ├── test_get.py
    ├── test_lib.py
    └── test_parse.py
```

The code is a library that generates and parses
[RaBe CRIDs](https://github.com/radiorabe/crid-spec) (Content Reference
Identifiers).  The public API is exposed via `cridlib.get()` and
`cridlib.parse()`.  Depending on the requested timestamp the `get()` function
delegates to one of three *strategy* modules that call different RaBe services
to discover the show name.


## 🔧 Build chain & CI

- **Continuous Integration** is GitHub Actions based; reusable workflows are
  referenced from the shared `radiorabe/actions` repository:
  - `.github/workflows/lint-and-test.yaml` – triggers on pushes to feature
    branches (not `main`, `develop`, or `gh-pages`); runs pre-commit and
    `pytest` via the shared `test-pre-commit` and `test-python-poetry`
    reusable workflows.
  - `.github/workflows/semantic-release.yaml` – triggers on pushes to `main`;
    bumps the version and creates a GitHub release based on conventional commit
    messages.
  - `.github/workflows/release.yaml` – triggers on pull requests, pushes to
    `main`, and release creation events; builds and publishes the Python
    package to PyPI via the shared `release-python-poetry` reusable workflow.

- **Release process** follows the [conventional commits
  standard](https://www.conventionalcommits.org/en/v1.0.0/).  Commit type
  `fix:` triggers a PATCH bump, `feat:` a MINOR bump, and a footer
  `BREAKING CHANGE:` a MAJOR bump.  All other types are allowed but do not
  trigger a release.  Once a commit lands on `main`, the release and PyPI
  publish happen automatically.


## 🧩 Code analysis

Key modules:

1. **`lib.py`** – defines the `CRID` class (scheme validation, authority
   check, version parsing, show slug extraction, media-fragment clock
   parsing), a `canonicalize_show()` helper using `python-slugify`, and the
   full error hierarchy (`CRIDError` and subclasses).

2. **`get.py`** – the main entry-point `get(timestamp, fragment)`.  Compares
   the requested timestamp to *now* and dispatches to `strategy.now`,
   `strategy.past`, or `strategy.future` to obtain the show name, then
   constructs and returns a `CRID`.

3. **`parse.py`** – thin wrapper around `CRID(value)` that provides the
   public `parse()` function.

4. **`util.py`** – `get_session()` returns a `requests.Session` pre-configured
   with exponential-backoff retry logic.

5. **`strategy/now.py`** – fetches the current show from the RaBe Songticker
   (`songticker.rabe.ch`) XML feed.

6. **`strategy/past.py`** – fetches a past show from the RAAR archive API
   (`archiv.rabe.ch`).

7. **`strategy/future.py`** – fetches a future show from the LibreTime
   live-info API (internal RaBe endpoint); covers at most seven days ahead.

Key characteristics:

- Fully type-annotated, linted with `ruff` (all rules enabled, see
  `ruff.toml`), and statically checked via `pytest-mypy` integrated into the
  test run.
- All external HTTP calls are made through `util.get_session()` and are
  mocked in tests with `requests_mock`.
- Show names are canonicalized to URL-safe slugs using `python-slugify`.
- Timestamps use `datetime` with explicit timezone awareness (`pytz` /
  `zoneinfo`).


## ✅ Tests & quality

- **Unit tests** use `pytest` with fixtures defined in `tests/conftest.py` and
  `tests/strategy/conftest.py`; `freezegun` is used for deterministic
  timestamps.

- External HTTP calls are fully mocked via `requests_mock` fixtures
  (`klangbecken_mock`, `archiv_mock`, `libretime_mock`, etc.), so the test
  suite runs entirely offline.  **Tests — including doctests — must never
  reach production APIs; always use `requests_mock` fixtures or
  `requests_mock.Mocker()` context managers instead.**

- The `pytest` configuration in `pyproject.toml` runs linting (`--ruff`),
  type-checking (`--mypy`), doctest extraction from Markdown files
  (`--doctest-glob='*.md'`) and module docstrings (`--doctest-modules`),
  and enforces **100 % code coverage** (`--cov-fail-under=100`).

- Tests are randomised (`--random-order`) to surface order-dependent failures.


## 🧠 Skills & knowledge required

Maintainers (and intelligent agents) should be comfortable with:

- **Python 3.12+** – typing, timezone handling (`zoneinfo` from the standard
  library for strategy modules, `pytz` as a third-party dependency used in
  tests and the `get()` docstring example), `datetime`, `pathlib`,
  `xml.etree.ElementTree`.
- **Poetry** for dependency management and publishing.
- **GitHub Actions** & conventional commits for CI/CD and releases.
- **pytest** with mocking, doctest, and plugins (`pytest-cov`, `pytest-mypy`,
  `pytest-ruff`, `pytest-random-order`, `freezegun`, `requests_mock`).
- **Libraries used**:
  - `requests` (with `HTTPAdapter` / `Retry`) for HTTP calls.
  - `uritools` for URI composition and splitting.
  - `python-slugify` for show-name canonicalization.
  - `pytz` / `zoneinfo` for timezone conversions.
- Familiarity with the [RaBe CRID spec](https://github.com/radiorabe/crid-spec)
  and [TV-Anytime media fragments](https://www.w3.org/TR/media-frags/).
- Understanding of the RaBe data sources: Songticker, RAAR archive, LibreTime.

Tests must **never** reach production APIs — all external HTTP calls must be
mocked.  No network access to RaBe services is required or permitted when
running the test suite.


## 🤖 Agentic tasks & guidelines

The following actions are good candidates for autonomous agents:

1. **Run the test suite** and verify 100 % coverage.  Always use
   `poetry run pytest` (or `poetry shell` + `pytest`) rather than installing
   packages system-wide; the lockfile ensures a reproducible environment.  If
   `pytest-mypy` reports missing stubs, add the appropriate `types-...`
   packages via `poetry add --group dev`.
2. **Lint and type-check** with `ruff` and the pytest plugins; propose fixes
   for violations.
3. **Dependency maintenance**: test upgrades and raise PRs or apply fixes.
   An agent can monitor the GitHub Advisory DB for security issues.
4. **Merge request review**: check for correctness, style, type annotations,
   and coverage.
5. **Documentation**: regenerate API docs via `mkdocs` / `docs/gen_ref_pages.py`;
   keep `README.md` examples in sync with the actual API.  Agents may update
   `AGENTS.md` itself.
6. **Environment setup**: ensure pre-commit hooks work (`pre-commit run
   --all-files`) and that `poetry install` produces a clean environment.

Agents must follow the existing conventional-commit rules when pushing
changes.


## 🚀 Getting started (for humans or agents)

```sh
# preferred: use Poetry to manage the environment
poetry install       # creates and populates a virtualenv automatically

# run all tests (linting, type-checking, doctests, coverage)
poetry run pytest

# lint only
poetry run ruff check .
poetry run ruff format --check .

# build documentation locally
poetry run mkdocs serve

# if you need interactive access
poetry shell
```


## 🗂️ Agent environment

Agents should run inside an environment that has:

- Python 3.12 (or newer) with all `poetry` dev dependencies installed via
  `poetry install`.
- Prefer **`poetry run`** when executing tests, linters or scripts rather
  than manually creating or activating venvs.
- Avoid system-wide `pip install` to prevent "externally managed" environment
  errors.
- Network access to GitHub and PyPI.
- Credential management (GitHub token, PyPI token) is handled via the
  `secrets` mechanism in GitHub Actions; agents must not hardcode secrets.

---

This file may be updated over time as new responsibilities arise or the
project evolves.  See `README.md` for user-facing instructions and refer back
here for agentic assistance guidelines.
