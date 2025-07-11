import pandas as pd
import os

from data.graph_config import GraphConfig, NetworkGraphConfig
from config import target_repositories
from functions.graph import plot_piechart, plot_network
from services.github import GitHubService
import functions.workflow as workflow
from functions.utility import cleanup

if __name__ == "__main__":
    github_token = os.environ.get("GITHUB_TOKEN")

    if not github_token:
        raise Exception("GITHUB_TOKEN environment variable is not set")
    
    github_service = GitHubService(github_token)

    repositories = target_repositories
    clone_dir = "cloned_repos"
    actions_all_repositories = []

    for repo in repositories:
        repo_path = github_service.clone_repo(repo, clone_dir)

        workflow_files = workflow.find_workflow_files(repo_path)

        actions_all_workflows = []

        for wf_file in workflow_files:
            workflow_actions = workflow.parse_workflow(repo_path.rstrip("/").split("/")[-1], wf_file, github_service)

            actions_all_repositories += workflow_actions
        
        cleanup(repo_path)
    
    cleanup(clone_dir)

    print("Latest actions table:")
    print(github_service.latest_actions_table)

    actions_df = pd.DataFrame(actions_all_repositories)

    print("Database:")
    print(actions_df)

    actions_of_interest = ["actions/checkout", "ruby/setup-ruby", "aws-actions/configure-aws-credentials"]

    for action in actions_of_interest:
        plot_piechart(
            f"select latest, version, count(*) as count from df where name = '{action}' group by name, version;", 
            GraphConfig(
                source = actions_df,
                x = "version",
                y = "count",
                title = f"Occurrences of different versions of {action} across repositories",
                output_path = f"graphs/{action.replace("/", "_").replace("-", "_")}_pie_chart.png",
                color_separation_variable="latest"
            )
        )

    plot_network(
        f"select repository, latest, name || '@' || version AS name_version from df;",
        NetworkGraphConfig(
            source = actions_df,
            root_node = "Organisation",
            layer_1 = "repository",
            layer_2 = "name_version",
            color_separation_variable = "latest",
            title = "GitHub Actions versions across repositories",
            output_path = "graphs/network_graph.png"
        )
    )