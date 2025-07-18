import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from main import (
    clone_repo,
    find_workflow_files,
    parse_workflow,
    analyze_github_actions
)
from data.repository_actions import GitHubAction, Workflow, RepositoryActions

class TestRepositoryFunctions(unittest.TestCase):

    @patch("main.subprocess.run")
    @patch("main.os.path.exists")
    def test_clone_repo_directory_exists(self, mock_exists, mock_run):
        mock_exists.return_value = True
        repo_url = "https://github.com/test/repo"
        expected_path = "cloned_repos/repo"

        path = clone_repo(repo_url)

        mock_run.assert_any_call(["rm", "-rf", expected_path], check=True)
        mock_run.assert_any_call(["git", "clone", "--depth", "1", repo_url, expected_path], check=True)
        self.assertEqual(path, expected_path)

    @patch("main.subprocess.run")
    @patch("main.os.path.exists")
    def test_clone_repo_directory_does_not_exist(self, mock_exists, mock_run):
        mock_exists.return_value = False
        repo_url = "https://github.com/test/repo"
        expected_path = "cloned_repos/repo"

        path = clone_repo(repo_url)

        mock_run.assert_called_once_with(["git", "clone", "--depth", "1", repo_url, expected_path], check=True)
        self.assertEqual(path, expected_path)

    @patch("main.Path.exists", return_value=False)
    def test_find_workflow_files_not_found(self, mock_exists):
        result = find_workflow_files("some/repo")

        self.assertEqual(result, [])

    @patch("main.Path.exists", return_value=True)
    @patch("main.glob.glob")
    def test_find_workflow_files_found(self, mock_glob, mock_exists):
        mock_glob.side_effect = [
            ["file1.yml"],
            ["file2.yaml"]
        ]
        result = find_workflow_files("some/repo")

        self.assertEqual(result, ["file1.yml", "file2.yaml"])

    def test_parse_workflow_valid(self):
        with patch("builtins.open", mock_open(read_data="""
        jobs:
            build:
                steps:
                - uses: actions/setup-python@v2
                - uses: actions/checkout@v3
        """
        )) as mock_file:
            result = parse_workflow("path/to/workflow.yml")

            self.assertIsInstance(result, Workflow)
            self.assertEqual(result.name, "workflow")
            self.assertEqual(len(result.actions), 2)
            self.assertEqual(result.actions[0], GitHubAction(name="actions/setup-python", version="v2"))

    def test_parse_workflow_invalid_yaml(self):
        with patch("builtins.open", mock_open(read_data=":::: invalid yaml ::::")):
            with self.assertRaises(Exception) as context:
                parse_workflow("invalid.yml")

        self.assertIn("Error parsing", str(context.exception))

    @patch("main.clone_repo")
    @patch("main.find_workflow_files")
    @patch("main.parse_workflow")
    def test_analyze_github_actions(self, mock_parse, mock_find, mock_clone):
        mock_clone.return_value = "cloned_repos/repo"
        mock_find.return_value = ["wf1.yml", "wf2.yaml"]
        mock_parse.side_effect = [
            Workflow(name="wf1", actions=[GitHubAction(name="act/one", version="v1")]),
            Workflow(name="wf2", actions=[GitHubAction(name="act/two", version="v2")])
        ]

        result = analyze_github_actions("https://github.com/user/repo")

        self.assertIsInstance(result, RepositoryActions)
        self.assertEqual(result.repository, "repo")
        self.assertEqual(len(result.workflows), 2)
        self.assertEqual(result.workflows[0].name, "wf1")
        self.assertEqual(result.workflows[1].actions[0].version, "v2")


if __name__ == '__main__':
    unittest.main()
