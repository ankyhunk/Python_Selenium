# Python_Selenium

Selenium WebDriver practice in Python: standalone demo scripts and a small pytest framework with page objects, run against the public practice sites at rahulshettyacademy.com and the-internet.herokuapp.com.

## Layout

- `pythonSel/test_*.py`: pytest tests (`conftest.py` holds the browser fixture and the failure-screenshot hook)
- `pageObjects/`: page objects used by the end-to-end test
- `data/`: test data for the parametrized end-to-end test
- `utils/`: shared helpers
- `pythonSel/*.py` and the root `*.py` files: standalone Selenium/openpyxl demo scripts

## Setup

Uses [uv](https://docs.astral.sh/uv/) and Python 3.13+. Selenium 4.6+ downloads the matching browser driver for you (Selenium Manager), so no chromedriver path is needed.

```bash
uv sync
```

## Running tests

```bash
uv run pytest                                # Chrome, visible window
uv run pytest --headless                     # Chrome, headless
uv run pytest --browser_name firefox         # Firefox
uv run pytest -m smoke --html=reports/report.html
```

Run a standalone script with `uv run python pythonSel/alerts.py`.

The tests use live public practice sites, so they need internet access and can fail when those sites change.
