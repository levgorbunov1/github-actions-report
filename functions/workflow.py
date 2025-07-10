from pathlib import Path
import glob
import yaml
from dataclasses import asdict

from data.github_action import GitHubAction
from services.github import GitHubService

def find_workflow_files(repo_path: str) -> list[str]:
    workflows_path = repo_path + "/.github/workflows"

    if not Path(workflows_path).exists():
        print(f"Can't find {repo_path}.github/workflows directory")
        return []

    print(f"searching {workflows_path} for workflows")

    return list(glob.glob(workflows_path + "/*.yml")) + list(glob.glob(workflows_path + "/*.yaml"))

def parse_workflow(repo_name: str, workflow_path: str, github_service: GitHubService) -> list[GitHubAction]:
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
                        actions.append(asdict(GitHubAction(repository=repo_name, workflow=workflow_name, name=name, version=version, latest=github_service.check_action_version(name, version))))

            return actions

    except yaml.YAMLError as e:
        raise Exception(f"Error parsing {workflow_path}: {e}")