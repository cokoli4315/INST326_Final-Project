"""Your project must include unit tests. For each function or method that does not perform input or output, your project should 
include enough test cases to verify that the function or method behaves as expected within the full range of 
expected conditions under which that function or method might be called. Provide enough comments, docstrings, and 
self-documenting code features (e.g., descriptive variable names) to make it clear what cases you are testing and why.
For any functions or methods that cannot be automatically tested, you are expected to provide a thorough written testing procedure. 
The written testing procedure should consist of precise instructions to a human tester about 
how to test each function or method that cannot be unit-tested and how to determine whether the test was successful.
Your unit tests (required) and written test procedure (if you write one) should be part of your Bitbucket or GitHub repository.
"""
# only need happy cases

from imdb.Person import Person
from imdb import Cinemagoer
import praw

# example code NOT IN FINAL
imdb = Cinemagoer()
movie = imdb.get_movie('0109830')
if movie.get('title') != "Forrest Gump":
    print('False')

# get access to reddit
reddit = praw.Reddit(
    client_id="my client id",
    client_secret="my client secret",
    user_agent="my user agent",
    username="my username",
    password="my password",
)

#get access to r/movies
movies_sub = reddit.subreddit("movies")
#goes through 10 most recent posts on r/movies and prints info about them
for submission in movies_sub.new(limit=10):
    print(submission.title)
    print(submission.score)
    print(submission.id)
    print(submission.url)