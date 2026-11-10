# Python Selenium

Selenium WebDriver practice in Python: a small pytest framework with page objects, plus standalone demo scripts for common Selenium tasks (locators, waits, alerts, frames, child windows, actions, tables, calendars, Excel upload/download).

## What it tests

All tests and scripts run against public practice sites:

- [rahulshettyacademy.com](https://rahulshettyacademy.com) — login page, ProtoCommerce shop (`/angularpractice`), GreenKart (`/seleniumPractise`), Automation Practice, dropdowns, upload/download page
- [the-internet.herokuapp.com](https://the-internet.herokuapp.com) — frames and multiple windows

The pytest suite covers:

| Test | What it checks |
| --- | --- |
| `test_e2eTestFramework.py::test_e2e` | Log in, add a product to the cart, check out, and confirm the order succeeds. Runs once per entry in the test data file. Marked `smoke`. |
| `test_SortingTables.py::test_sort` | Sorting the GreenKart offers table by name gives an alphabetical list. |

## Tech stack

| Tool | Version |
| --- | --- |
| Python | 3.13+ |
| Selenium | 4.52.0 (Selenium Manager downloads the browser driver) |
| pytest | 9.2.0 |
| pytest-html | 4.2.0 (HTML reports with failure screenshots) |
| openpyxl | 3.1.5 (Excel demo scripts) |
| uv | package and environment manager |

Exact versions are pinned in `uv.lock`.

## Project structure

```
.
├── pythonSel/
│   ├── conftest.py               # browser fixture, CLI options, failure-screenshot hook
│   ├── test_e2eTestFramework.py  # end-to-end shop test (page objects + test data)
│   ├── test_SortingTables.py     # table sorting test
│   └── *.py                      # standalone demo scripts (alerts, frames, waits, ...)
├── pageObjects/
│   ├── login.py                  # LoginPage
│   ├── shop.py                   # ShopPage
│   └── checkout_confirmation.py  # Checkout_Confirmation
├── utils/
│   └── browserutils.py           # BrowserUtils base class
├── data/
│   └── test_e2eTestFramework.json  # login and product data for test_e2e
├── *.py                          # more standalone demos (calendar, Excel upload/download)
├── pytest.ini                    # test path, import path, markers
├── pyproject.toml                # dependencies
└── uv.lock
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (it installs Python 3.13 for you if needed)
- Google Chrome; Firefox too if you use `--browser_name firefox` or the Firefox demo scripts (`childWindow.py`, `framesDemo.py`)
- Internet access (the tests use live sites)

No chromedriver or geckodriver download is needed.

## Install

```bash
uv sync
```

## Run the tests

All tests (Chrome, visible window):

```bash
uv run pytest
```

Headless:

```bash
uv run pytest --headless
```

One file, or one test:

```bash
uv run pytest pythonSel/test_SortingTables.py
uv run pytest pythonSel/test_e2eTestFramework.py::test_e2e
```

Only tests marked `smoke`:

```bash
uv run pytest -m smoke
```

In Firefox:

```bash
uv run pytest --browser_name firefox
```

To run in parallel, add the `pytest-xdist` plugin and pass `-n`:

```bash
uv run --with pytest-xdist pytest -n 2
```

Run a standalone demo script:

```bash
uv run python pythonSel/alerts.py
```

## Reports

Generate an HTML report:

```bash
uv run pytest --html=reports/report.html
```

- The report is written where `--html` points, relative to where you run the command (`reports/report.html` above).
- When a test fails, a screenshot is saved to `pythonSel/reports/` and embedded in the HTML report.

Both folders are git-ignored.

## Test data and config

`data/test_e2eTestFramework.json` drives `test_e2e`. Each entry is one test run:

```json
{
  "data": [
    {
      "userEmail": "<practice-site-username>",
      "userPassword": "<practice-site-password>",
      "productName": "Blackberry"
    }
  ]
}
```

Use the demo username and password shown on the [login practice page](https://rahulshettyacademy.com/loginpagePractise/). The site changes its demo password from time to time; if login fails, update this file.

The Excel scripts (`upload.py`, `ed.py`, `excelDemo.py`) read and write `download.xlsx` in your `Downloads` folder.

Do not put real credentials in this repo. Keep any private values in a `.env` file, which is git-ignored.

