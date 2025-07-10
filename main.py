import pandas as pd
import os

from data.graph_config import GraphConfig
from config import target_repositories
from functions.graph import plot_piechart
from services.github import GitHubService
import functions.workflow as workflow


if __name__ == "__main__":
    repositories = target_repositories
    github_service = GitHubService(os.environ.get("GITHUB_TOKEN"))

    actions_all_repositories = []

    for repo in repositories:
        repo_path = github_service.clone_repo(repo)

        workflow_files = workflow.find_workflow_files(repo_path)

        actions_all_workflows = []

        for wf_file in workflow_files:
            workflow_actions = workflow.parse_workflow(repo_path.rstrip("/").split("/")[-1], wf_file, github_service)

            actions_all_repositories += workflow_actions

    print("Latest actions table:")
    print(github_service.latest_actions_table)

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