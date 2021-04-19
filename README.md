# About 

This project creates a `repos.json` that can be utilized by the [GitHub Repository Profiler](https://github.com/rajasoun/github-repository-profiler). 

The current approach assumes that the repos that you want to show in the portal are:
1. available in a GitHub organization, and 
1. they all are tagged with a certain _topic_.

## Installation

`pip install -r requirements.txt`

## Usage

1. Copy `.env-example` to `.env`
1. Fill out the `.env` file with a _token_ from a user that has access to the organization to scan (listed below)
1. Fill out the `.env` file with the exact _topic_ name you are searching for
1. Fill out the `.env` file with the exact _organization_ that you want to search in
1. Run `python3 ./crawler.py`, which will create a `repos.json` file containing the relevant metadata for the GitHub repos for the given _topic_
1. Copy `repos.json` to your instance of the [GitHub Repository Profiler](https://github.com/rajasoun/github-repository-profiler) and launch the portal as outlined in their installation instructions
