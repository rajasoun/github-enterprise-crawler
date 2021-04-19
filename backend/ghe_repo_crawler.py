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
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os


if __name__ == "__main__":
    os = load_secrets_from_dot_env()
    gh_session = create_enterprise_session(os.getenv("GH_URL"), os.getenv("GH_TOKEN"))
    print(gh_session.me())
