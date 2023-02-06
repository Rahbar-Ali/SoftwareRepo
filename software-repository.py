import json
import subprocess
import os


def process_git_repo(repo_path):
    result = subprocess.run(["git", "log", "--pretty=format:\"%H\""], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    commits = result.stdout.strip().split("\n")

    tests_of_commits = []
    for commit in commits:
        result = subprocess.run(["git",  "show", "--pretty=format:\"\"", "--name-only", commit], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        files = result.stdout.strip().split("\n")
        test_classes = [file for file in files if file.endswith(".java") and file.startswith("src/test/")]
        num_of_test_classes = len(test_classes)

        result = subprocess.run(["grep", "-r", "public void test", "src/test/"], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")
        test_methods = [line.split(":")[0] for line in lines]
        num_of_test_methods = len(test_methods)

        tests_of_commit = {
            "commit": commit,
            "num_of_test_classes": num_of_test_classes,
            "num_of_test_methods": num_of_test_methods,
            "list_of_test_classes": test_classes,
            "list_of_test_methods": test_methods,
        }   
        tests_of_commits.append(tests_of_commit)


    data = {
        "location": repo_path,
        "number_of_commits": len(commits), 
        "tests_of_commits": tests_of_commits,
    }
    return data

repo_path = "C:/Users/hp/Desktop/Git 2/home-repair-system"

if os.path.exists(repo_path) and os.path.isdir(repo_path):
    data = process_git_repo(repo_path)
    with open("output.json", "w") as f:
        json.dump(data, f, indent=2)
else:
    print(f"The directory {repo_path} does not exist or is not a valid directory.")
