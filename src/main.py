import os
import sys
import datetime
from github import Github
from github_context import GithubContext

if __name__ == "__main__":

    github_token = os.environ["INPUT_REPO_TOKEN"]
    release_id = os.environ.get("INPUT_RELEASE-ID")

    context = GithubContext()

    if release_id is None:
        try:
            release_id = context.payload["release"]["id"]
        except KeyError:
            sys.stderr.write("Cannot find Release ID!\n")
            exit(1)

    cli = Github(github_token)
    repo_name = "{}/{}".format(context.repo()["owner"], context.repo()["repo"])
    sys.stdout.write("Getting repo information...")
    repo = cli.get_repo(repo_name)
    sys.stdout.write("[DONE]\n")

    sys.stdout.write("Getting release information...")
    release = repo.get_release(release_id)
    sys.stdout.write("[DONE]\n")

    sys.stdout.write("Updating body...")
    author_info = "<img src='{}' width='20' height='20'/> [{}]({})".format(
        context.payload["sender"]["avatar_url"],
        context.payload["sender"]["login"],
        context.payload["sender"]["html_url"]
    )
    deployed_on = datetime.datetime.now().strftime("%d/%m/%Y %H:%I:%S")
    new_body = """{}

## Deployment Information
|  | Info |
|--------------|-------------------------------|
| Deployed on | {} |
| Action URL | https://github.com/{}/actions/runs/{} |
| Released by | {} |
""".format(release.body, deployed_on, repo_name, context.run_id, author_info)
    release.update_release(name=release.title, message=new_body)
    sys.stdout.write("[DONE]\n")
