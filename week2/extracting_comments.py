import csv
from github import Github, GithubException
import time

# Provide your access_token
access_token = input("Please enter your Github Personal access token: ")
# Create a Github instance with your access_token
g = Github(access_token)

# Get the repository
owner = input("Repo Owner in github url:")
repo_name = input("Repo Name in github url:")
repo = g.get_repo(owner + "/" + repo_name)

# Get all the pull requests
pulls = repo.get_pulls(state='all')

# Create a CSV file to store the pull request information
with open('pull_requests.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Pull Request Number', 'Title', 'Merged', 'Time to Merge', 'Comments', 'Review Comments', 'Comment Messages',
         'Review Messages', 'Lines of Code Changed'])

    # Iterate through each pull request
    for pull in pulls:
        print('wait')
        merged = "Yes" if pull.merged else "No"
        time_to_merge = pull.merged_at - pull.created_at if pull.merged else None
        comments_count = pull.comments
        review_comments_count = pull.review_comments
        files_changed = pull.get_files()
        lines_added = 0
        lines_deleted = 0
        for file in files_changed:
            lines_added += file.additions
            lines_deleted += file.deletions

        comment_messages = []
        review_messages = []
        try:
            # Get the comments for the pull request
            comments = pull.get_comments()
            for comment in comments:
                comment_messages.append(comment.body)

            # Get the review comments for the pull request
            reviews = pull.get_reviews()
            for review in reviews:
                review_messages.append(review.body)

        except GithubException as e:
            # Handle rate limit error
            if e.status == 403:
                print("Rate limit exceeded. Sleeping for 60 seconds.")
                time.sleep(60)
                continue
            else:
                print("Error getting comments for pull request", pull.number, e.status)
                continue

        # Write the pull request information to the CSV file
        writer.writerow(
            [pull.number, pull.title, merged, time_to_merge, comments_count, review_comments_count, comment_messages,
             review_messages, lines_added + lines_deleted])
