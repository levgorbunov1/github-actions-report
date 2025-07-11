from github import Github
import os
import subprocess
import pandas as pd
import pandasql as ps

from data.github_action import GitHubActionTag

class GitHubService():

    def __init__(self, token):
        self.latest_actions_table = pd.DataFrame(columns=['name', 'tag', 'sha'])
        self.gh_client = Github(token)

    def clone_repo(self, repo_url: str, clone_dir: str) -> str:   
        cloned_repo_dir = f"{clone_dir}/{repo_url.rstrip("/").split("/")[-1]}"

        if os.path.exists(cloned_repo_dir):
            print(f"Directory {cloned_repo_dir} already exists, it will be recreated") 
            subprocess.run(["rm", "-rf", cloned_repo_dir], check=True)

        print(f"Cloning {repo_url} to {cloned_repo_dir}")     
        subprocess.run(["git", "clone", "--depth", "1", repo_url, cloned_repo_dir], check=True)

        return cloned_repo_dir
    
    def check_action_version(self, name, version):
        try:
            if len(name.split("/")) > 2:
                repo_name = "/".join(name.split("/")[:2])
            else:
                repo_name = name

            query_result = ps.sqldf(f"select * from df where name = '{name}'", {'df': self.latest_actions_table})

            if query_result.empty:
                latest_tag = self.gh_client.get_repo(repo_name).get_tags()[0]

                self.latest_actions_table.loc[len(self.latest_actions_table)] = [name, latest_tag.name, latest_tag.commit.sha]

                latest_tag = GitHubActionTag(name=name, tag=latest_tag.name, sha=latest_tag.commit.sha)
            else:
                latest_tag = GitHubActionTag(**query_result.iloc[0].to_dict())

            if version == latest_tag.tag or version == latest_tag.sha or version == "main":
                return True

            return False
        
        except Exception as e:
            print(f"Error fetching tags for {name}: {e}")