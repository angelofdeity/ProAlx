from datetime import datetime, timedelta
from flask import jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from dotenv import load_dotenv
from api.v1.views import app_views
import requests
from models import storage
load_dotenv()

alx_repos = ['AirBnB_clone', 'AirBnB_clone_v2', 'AirBnB_clone_v3',
             'AirBnB_clone_v4',
             'alx-higher_level_programming', 'alx-low_level_programming',
             'alx-system_engineering-devops', 'simple_shell',
             'binary_trees', 'sorting_algorithms', 'alx-zero_day',
             'monty', 'RSA-Factoring-Challenge']


@jwt_required
@app_views.route('/users/<user_id>/daily_commits', strict_slashes=False)
def get_daily_commits(id, n=7):
    """
    Calculate the daily commit count for each date based on the commit data.

    Returns:
        dict: A dictionary containing the commit counts per day and repository.
    """
    if id != get_jwt_identity():
        abort(401)
    user = storage.get('User', id)
    token = user.gh_access_token
    username = user.github_login
    return get_commits(token, username, n)


def get_commits(token, username, n=7):
    """
    Fetches the commit counts per day and repository for the last n days.
    Args:
        token (str): User access token for authentication.
        username (str): GitHub username.

    Returns:
        dict: A dictionary containing the commit counts per day and repository.
        Example:
        {
            "2023-05-18": {
                "repo1": 3,
                "repo2": 2
            },
            "2023-05-19": {
                "repo1": 1,
                "repo3": 5
            },
            ...
        }
    """
    # Calculate the date range for the last 7 days
    today = datetime.now().date()
    week_ago = today - timedelta(days=n)

    # Format the date strings
    today_str = today.isoformat()
    week_ago_str = week_ago.isoformat()
    url = (
        f"https://api.github.com/search/commits?q=author:{username}"
        f"+author-date:{week_ago_str}..{today_str}"
    )
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    contributions = data["items"]

    # dictionary to store the commit counts per day and repository
    commit_counts = {}

    for contribution in contributions:
        repo_name = contribution["repository"]["full_name"]
        if username in repo_name:
            repo_name = repo_name.replace(f'{username}/', '')
        # Extract the date part only
        commit_date = contribution["commit"]["author"]["date"][:10]
        # Check if the commit date is already in the dictionary
        if commit_date in commit_counts:
            # Check if the repository is already in the commit counts for the given date
            if repo_name in commit_counts[commit_date]:
                # Increment the commit count for the repository
                commit_counts[commit_date][repo_name] += 1
            else:
                # Add the repository to the commit counts for the given date
                commit_counts[commit_date][repo_name] = 1
        else:
            # Add the commit date and repository to the commit counts dictionary
            commit_counts[commit_date] = {repo_name: 1}
    return jsonify(commit_counts)
