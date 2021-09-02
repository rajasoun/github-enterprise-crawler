#!/usr/bin/env python3

import github3


def create_enterprise_session(url, token=None):
    """
    Create a github3.py session for a GitHub Enterprise instance

    If token is not provided, will attempt to use the GH_TOKEN
    environment variable if present.
    """

    session = github3.github.GitHubEnterprise(url=url, token=token)

    if session is None:
        msg = "Unable to connect to GitHub Enterprise (%s) with provided token."
        raise RuntimeError(msg, url)

    return session


def load_secrets_from_dot_env():
    """
    Load secrets from .env file

    Ensure .env file is ignored in .gitignore.
    """
    import os
    from os.path import dirname, join
    from dotenv import load_dotenv
    # Load env variables from file
    dotenv_path = join(dirname(__file__), "../.env")
    load_dotenv(dotenv_path)
    return os


def log_user(gh_session):
    print(gh_session.me())


def crawl_repos_for_commit(gh_session, os):
    """
    Get Repositories for the GitHub Organization by Topic

    Ensure Topic is configured with automatic-profiler
    """
    # Set the topic
    topic = os.getenv("TOPIC")
    organization = os.getenv("ORGANIZATION")

    # Get all repos from organization
    search_string = "org:{} topic:{}".format(organization, topic)
    all_repos = gh_session.search_repositories(search_string)

    repo_list = []
    for repo in all_repos:
        if repo is not None:
            print("{0}".format(repo.repository))
            repo.repository.refresh()
            repo_profile = repo.as_dict()
            repo_profile["_InnerSourceMetadata"] = {}

            # fetch repository participation
            participation = repo.repository.weekly_commit_count()
            repo_profile["_InnerSourceMetadata"]["participation"] = participation[
                "all"
            ]
            # fetch repository topics
            topics = repo.repository.topics()
            repo_profile["_InnerSourceMetadata"]["topics"] = topics.names
            repo_list.append(repo_profile)
        return repo_list


def convert_to_json(repo_list):
    import json
    # Write each repository to a repos.json file
    with open("repos.json", "w") as f:
        json.dump(repo_list, f, indent=4)


if __name__ == "__main__":
    os = load_secrets_from_dot_env()
    gh_session = create_enterprise_session(
        os.getenv("GH_URL"), os.getenv("GH_TOKEN"))
    log_user(gh_session)
    repo_list = crawl_repos_for_commit(gh_session, os)
    convert_to_json(repo_list)
