# RedditVoteCounter

A bot counts votes made as top-level comments on a post. Counts votes by looking for comments which include one of a series of keywords. Originally designed for use in [this /r/brisbane thread](https://old.reddit.com/r/brisbane/comments/14910v9/important_the_future_of_rbrisbane/).

Ignores the votes from users who have not participated in the subreddit recently, as well as users who have double-voted. 

For users who have inadvertently used two or more keywords, it prints out the text of their comment for manual counting.


## How to run your own

1. Install PRAW. [See the PRAW website for instructions](https://praw.readthedocs.io/en/latest/getting_started/installation.html). RedditVoteCounter is written targetting PRAW 7.5 and Python 3.8.
2. Created a Reddit authorised app [here](https://www.reddit.com/prefs/apps/)
3. Give the bot a name of your choosing, set its type to "script", leave the about url blank or point to this repo. Add a description if you want, and set the redirect uri to http://localhost:8080.
4. Make a note of the `client_id`, which is the number found under the words "personal use script", under the name of your bot, once you have created the app. Also note your `secret`.
5. Create a `praw.ini` file in the same directory as this application, formatted as shown. `username` and `password` refer to the user account you wish to run the bot under.
```ini
[RedditVoteCounter]
username=<username>
password=<password>
client_id=<client_id>
client_secret=<secret>
```
6. Edit `reddit_vote_counter.py` to include the desired parameters on the lines near the bottom of the file.
7. Run the script `python reddit_vote_counter.py`
