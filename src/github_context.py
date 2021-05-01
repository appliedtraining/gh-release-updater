import os
import json
from typing import Union


class GithubContext:
    def __init__(self):
        self.payload = {}
        if os.path.exists(os.environ["GITHUB_EVENT_PATH"]):
            with open(os.environ["GITHUB_EVENT_PATH"], "rb") as f:
                self.payload = json.load(f)
        else:
            path = os.environ["GITHUB_EVENT_PATH"]
            print(f"GITHUB_EVENT_PATH ${path} does not exist")

        self.event_name = os.environ["GITHUB_EVENT_NAME"]
        self.sha = os.environ["GITHUB_SHA"]
        self.ref = os.environ["GITHUB_REF"]
        self.workflow = os.environ["GITHUB_WORKFLOW"]
        self.action = os.environ["GITHUB_ACTION"]
        self.actor = os.environ["GITHUB_ACTOR"]
        self.job = os.environ["GITHUB_JOB"]
        self.run_number = int(os.environ["GITHUB_RUN_NUMBER"])
        self.run_id = int(os.environ["GITHUB_RUN_ID"])

    def repo(self) -> Union[dict, Exception]:
        if os.environ.get("GITHUB_REPOSITORY"):
            (owner, repo) = os.environ.get("GITHUB_REPOSITORY").split("/")
            return {"owner": owner, "repo": repo}

        if self.payload.get("repository"):
            return {
                "owner": self.payload["repository"]["owner"]["login"],
                "repo": self.payload["repository"]["name"]
            }

        raise Exception("context.repo requires a GITHUB_REPOSITORY environment variable like 'owner/repo'")
