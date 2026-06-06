# Hotel Planisphere – Automated Testing Project


## Setup & Run Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install browser
playwright install chromium

# 3. Run all tests
pytest

# 4. Run with HTML report
pytest --html=reports/report.html --self-contained-html

# 5. Run specific suite
pytest tests/test_login.py -v

# 6. Run single test
pytest tests/test_login.py::TestLoginFunctional::test_TC_L_01_valid_premium_user_login -v
```
