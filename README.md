# GitHub Actions Report
Produces a report, displaying data on which GitHub Actions and Workflows are being used across your repositories.

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

### Feature Ideas

- ThreadPools for asynchronous task processing to boost performance.
- Handling reusable workflows.
- Handling duplicate actions in a workflow.