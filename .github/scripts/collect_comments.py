import os
import requests
import csv
import sys

def collect_comments(pr_number):
    # GitHub API endpoint to get comments on a pull request
    url = f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/pulls/{pr_number}/reviews'

    # GitHub token for authentication
    headers = {'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'}

    # Make a request to the GitHub API
    response = requests.get(url, headers=headers)
    reviews = response.json()

    # Extract comments from reviews
    comments = [comment['body'] for review in reviews if 'comments' in review for comment in review['comments']]

    # Export comments to a CSV file
    with open('comments.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Comment'])
        csv_writer.writerows([[comment] for comment in comments])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: collect_comments.py <PR_NUMBER>")
        sys.exit(1)

    pr_number = int(sys.argv[1])
    collect_comments(pr_number)
