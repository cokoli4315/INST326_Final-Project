"""at least 1 class, 8 functions
1. Get access to titles of posts in r/movies
2. take in title of post and look for actor's name using regex
3. if a name is found, look through imdb for actor's page
4. if a page is found create an instance of Actor that gets info from imdb page
5. take the Actor instance and create a string with their info
        5. After the match is found, analyze our results using pandas to better understand the information.
6. comment string to reddit post
"""
from imdb.Person import Person
from imdb import Cinemagoer
import praw

class Actor:
    """will hold information about an actor.
    
    Attributes:
        name
        age
        date of birth
        place of birth
        movies (list)
        awards (list)"""
    #ask if counts as function
    def __init__(self, imdb_page):
        pass

