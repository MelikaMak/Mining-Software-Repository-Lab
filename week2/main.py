import csv
from github import Github

# Provide your access_token

access_token = input("Please enter your Github Personal access token: ")
# Create a Github instance with your access_token
g = Github(access_token)

# Get the repository
owner = input("Repo Owner in github url:")
repo_name = input("Repo Name in github url:")
repo = g.get_repo(owner+"/"+repo_name)

# Get all the pull requests
pulls = repo.get_pulls(state='all')

# Create a CSV file to store the pull request information
with open('pull_requests.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Pull Request Number', 'Title', 'Merged', 'Time to Merge', 'Comments', 'Review Comments', 'Lines of Code Changed'])

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

        # Write the pull request information to the CSV file
        writer.writerow([pull.number, pull.title, merged, time_to_merge, comments_count, review_comments_count, lines_added + lines_deleted])
