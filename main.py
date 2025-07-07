import os
import subprocess
from pathlib import Path
import glob

def clone_repo(repo_url: str, clone_dir: str = "cloned_repos") -> str:   
    cloned_repo_dir = f"{clone_dir}/{repo_url.rstrip("/").split("/")[-1]}"

    if os.path.exists(cloned_repo_dir):
        print(f"Directory {cloned_repo_dir} already exists, it will be recreated") 
        subprocess.run(["rm", "-rf", cloned_repo_dir], check=True)

    print(f"Cloning {repo_url} to {cloned_repo_dir}")     
    subprocess.run(["git", "clone", repo_url, cloned_repo_dir], check=True)

    return cloned_repo_dir

def find_workflow_files(repo_path: str) -> list[Path]:
    workflows_path = repo_path + "/.github/workflows"

    if not Path(workflows_path).exists():
        print(f"Can't find {repo_path}.github/workflows directory")
        return []

    print(f"searching {workflows_path} for workflows")

    return list(glob.glob(workflows_path + "/*.yml")) + list(glob.glob(workflows_path + "/*.yaml"))

def analyze_github_actions(repo_url: str) -> tuple[list[str], list[str]]:
    repo_path = clone_repo(repo_url)
    workflow_files = find_workflow_files(repo_path)


if __name__ == "__main__":
    repo_url = "https://github.com/levgorbunov1/my-eks-cluster"
    analyze_github_actions(repo_url)
