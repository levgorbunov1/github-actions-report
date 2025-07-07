import subprocess
import os

def clone_repo(repo_url: str, clone_dir: str = "cloned_repos") -> str:   
    cloned_repo_dir = f"{clone_dir}/{repo_url.rstrip("/").split("/")[-1]}"

    if os.path.exists(cloned_repo_dir):
        print(f"Directory {cloned_repo_dir} already exists, it will be recreated") 
        subprocess.run(["rm", "-rf", cloned_repo_dir], check=True)

    print(f"Cloning {repo_url} to {cloned_repo_dir}")     
    subprocess.run(["git", "clone", repo_url, cloned_repo_dir], check=True)

    return cloned_repo_dir

if __name__ == "__main__":
    repo_url = "https://github.com/levgorbunov1/my-eks-cluster"
    repo_path = clone_repo(repo_url)