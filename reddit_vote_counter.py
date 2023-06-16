import praw
from datetime import datetime

# Set up PRAW with your Reddit API credentials
reddit = praw.Reddit(
    "RedditVoteCounter",
    user_agent=f"praw:RedditVoteCounter:1.0.0 (by /u/{username})",
)

def check_user_history(username, subreddit, cutoff_date, start_date):
    user = reddit.redditor(username)
    for comment in user.comments.new(limit=400):
        if comment.subreddit.display_name.lower() == subreddit.lower():
            comment_date = datetime.utcfromtimestamp(comment.created_utc).date()
            if comment_date < cutoff_date and comment_date > start_date:
                return True
    return False

def count_comments_with_keywords(submission_url, keywords, subreddit, cutoff_date, start_date):
    submission = reddit.submission(url=submission_url)
    double_keywords = []
    excluded = 0
    none = 0
    duplicate_users = set()
    keyword_counts = {keyword: 0 for keyword in keywords}
    users_seen = set()

    submission.comments.replace_more(limit=None)  # Retrieve all top-level comments

    iterator = 1
    for comment in submission.comments:
        print(iterator)
        iterator += 1
        comment_author = comment.author
        if comment_author and comment_author.name not in users_seen:
            users_seen.add(comment_author.name)
            if check_user_history(comment_author.name, subreddit, cutoff_date, start_date):
                comment_text = comment.body.lower()
                keyword_matches = [keyword for keyword in keywords if keyword in comment_text]
                if len(keyword_matches) >= 2:
                    double_keywords.append(comment.body)
                elif len(keyword_matches) == 1:
                    keyword_counts[keyword_matches[0]] += 1
                else:
                    none += 1
            else:
                excluded += 1
        elif comment_author and comment_author.name in users_seen:
            duplicate_users.add(comment_author.name)

    print("Keyword counts:")
    for keyword, count in keyword_counts.items():
        print(f"Number of comments containing '{keyword}': {count}")
    print(f"Number of comments containing at least two keywords: {len(double_keywords)}")
    print(f"Number of users excluded for not being from around here: {excluded}")
    print(f"Number of users excluded for failing to provide any keywords: {none}")
    print("Users who left more than one top-level comment:")
    for user in duplicate_users:
        print(user)
    print("Comments containing at least two keywords:")
    for comment in double_keywords:
        print(comment)
        print("*****")


# Example usage:
submission_url = "https://old.reddit.com/r/brisbane/comments/14910v9/important_the_future_of_rbrisbane/"
keywords = ["dark", "stay", "don't care"]
subreddit = "brisbane"
cutoff_date = datetime.strptime("2023-06-11", "%Y-%m-%d").date()
start_date = datetime.strptime("2021-12-01", "%Y-%m-%d").date()
username = "<YOUR USERNAME>"

count_comments_with_keywords(submission_url, keywords, subreddit, cutoff_date, start_date)
