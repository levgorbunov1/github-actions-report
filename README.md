# GitHub Actions Report
Produces a report, displaying data on which GitHub Actions and Workflows are being used across your repositories.

You can see the report [here](github_actions_report.md).

### venv setup 

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### GitHub service setup

Export your GitHub token that you want to use with the GitHub REST API: `export GITHUB_TOKEN=my_token`

### Run script

- Configure list of [target repositories](config.py).
- Run the script: `python main.py`

### Unit tests

 `python -m unittest test_main.py`