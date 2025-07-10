import os
import glob
import json
import subprocess
import pandas as pd
from pathlib import Path
import yaml
from dataclasses import asdict

from data.github_action import GitHubAction
from data.graph_config import GraphConfig
from config import target_repositories
from functions.graph import plot_piechart


def clone_repo(repo_url: str, clone_dir: str = "cloned_repos") -> str:   
    cloned_repo_dir = f"{clone_dir}/{repo_url.rstrip("/").split("/")[-1]}"

    if os.path.exists(cloned_repo_dir):
        print(f"Directory {cloned_repo_dir} already exists, it will be recreated") 
        subprocess.run(["rm", "-rf", cloned_repo_dir], check=True)

    print(f"Cloning {repo_url} to {cloned_repo_dir}")     
    subprocess.run(["git", "clone", "--depth", "1", repo_url, cloned_repo_dir], check=True)

    return cloned_repo_dir

def find_workflow_files(repo_path: str) -> list[str]:
    workflows_path = repo_path + "/.github/workflows"

    if not Path(workflows_path).exists():
        print(f"Can't find {repo_path}.github/workflows directory")
        return []

    print(f"searching {workflows_path} for workflows")

    return list(glob.glob(workflows_path + "/*.yml")) + list(glob.glob(workflows_path + "/*.yaml"))

def parse_workflow(repo_name: str, workflow_path: str) -> list[GitHubAction]:
    workflow_name = Path(workflow_path).stem

    actions = []

    try:
        with open(workflow_path, 'r') as f:
            data = yaml.safe_load(f)

            for job in data.get("jobs", {}).values():
                for step in job.get("steps", []):
                    uses = step.get("uses")

                    if uses:
                        name, version = uses.split("@", 1)
                        actions.append(asdict(GitHubAction(repository=repo_name, workflow=workflow_name, name=name, version=version)))

            return actions

    except yaml.YAMLError as e:
        raise Exception(f"Error parsing {workflow_path}: {e}")

def analyze_github_actions(repo_url: str) -> list[GitHubAction]:
    repo_path = clone_repo(repo_url)

    workflow_files = find_workflow_files(repo_path)

    actions_all_workflows = []

    for wf_file in workflow_files:
        workflow_actions = parse_workflow(repo_url.rstrip("/").split("/")[-1], wf_file)
        actions_all_workflows += workflow_actions

    return actions_all_workflows


if __name__ == "__main__":
    repositories = target_repositories

    actions_all_repositories = []

    for repo in repositories:
        repository_actions = analyze_github_actions(repo)

        actions_all_repositories += repository_actions

    df = pd.DataFrame(actions_all_repositories)

    print("Database:")
    print(df)

    actions_of_interest = ["actions/checkout", "ruby/setup-ruby", "hashicorp/setup-terraform"]

    for action in actions_of_interest:
        plot_piechart(
            f"select version, count(*) as count from df where name = '{action}' group by name, version;", 
            GraphConfig(
                source = df,
                x = "version",
                y = "count",
                title = f"Variation in {action} version",
                output_path = f"graphs/{action.replace("/", "_").replace("-", "_")}_pie_chart.png"
            )
        )