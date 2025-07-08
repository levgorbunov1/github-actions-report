import os
import glob
import subprocess
from pathlib import Path
import json
import yaml
from dataclasses import asdict
from data.repository_actions import GitHubAction, Workflow, RepositoryActions


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

def parse_workflow(file_path: str) -> Workflow:
    workflow_name = Path(file_path).stem

    actions = []

    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

            for job in data.get("jobs", {}).values():
                for step in job.get("steps", []):
                    uses = step.get("uses")

                    if uses:
                        name, version = uses.split("@", 1)
                        actions.append(GitHubAction(name=name, version=version))

            return Workflow(name=workflow_name, actions=actions)

    except yaml.YAMLError as e:
        raise Exception(f"Error parsing {file_path}: {e}")

def analyze_github_actions(repo_url: str) -> RepositoryActions:
    repo_path = clone_repo(repo_url)
    repo_name = repo_url.rstrip("/").split("/")[-1]

    workflow_files = find_workflow_files(repo_path)

    workflows = []

    for wf_file in workflow_files:
        workflow = parse_workflow(wf_file)
        workflows.append(workflow)

    return RepositoryActions(repository=repo_name, workflows=workflows)


if __name__ == "__main__":
    repositories = [
        "https://github.com/levgorbunov1/my-eks-cluster",
        "https://github.com/alphagov/tech-docs-monitor",
        "https://github.com/alphagov/govuk-infrastructure"
    ]

    for repo in repositories:
        repository_actions = analyze_github_actions(repo)

        repo_json = json.dumps(asdict(repository_actions), indent=2)

        print(f"✅ Repository Actions for {repo}:\n\n{repo_json}")