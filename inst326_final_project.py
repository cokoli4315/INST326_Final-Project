# ask if check in 1 needs all 8 functions
"""at least 1 class, 8 functions
1. Get access to titles of posts in r/movies
2. take in title of post and look for actor's name using regex
3. if a name is found, look through imdb for actor's page
4. if a page is found create an instance of Actor that gets info from imdb page
5. take the Actor instance and create a string with their info
        After the match is found, analyze our results using pandas to better understand the information.
6. comment string to reddit post
"""
from imdb.Person import Person
from imdb import Cinemagoer
import praw

class Actor:
    """will hold information about an actor.
    
    Attributes:
        name (str)
        age (int)
        date of birth (str)
        place of birth (str)
        movies (list): btwn 3-5 movies
        awards (list): btwn 3-5 awards"""
    # ask if init counts as a function
    def __init__(self, person_id):
        """Sets the attributes for the Actor."""
        pass
    
    def get_popular_movies(self, person_id):
        """gets 3-5 of the most popular movies of the actor"""
        pass
    
    def get_recent_awards(self, person_id):
        """gets 3-5 of the most recent awards the actor won"""
        pass

def get_post(subreddit):
    """Gets access to each post in r/movies
    
    Args:
        subreddit: the subreddit we are looking through"""
    pass

def get_title(post_id):
    """access each of the titles of each post"""
    pass

def find_actor_name():
    """take in title of post and look for actor's name using regex"""
    pass

def find_actor_page():
    """if a name is found, look through imdb for actor's page"""
    pass

def create_comment(actor):
    """take the Actor instance and create a string with their info
    
    Args:
        actor (Actor): the actor the comment is going to be about
        
    Returns:
        comment (str): a string with the complete info about the actor"""
    pass

def publish_comment(post_id, comment):
    """comment string to reddit post
    
    Args:
        post_id: post id that has the actor's name in it
        comment: the comment that will be published"""
    pass

def main():
    """ goes through calls get_posts, calls get_title() for each post, calls find_actor_name() for title, if an actor's name is found 
    calls find_actor_page, if a page for the actor is found creates an Actor instance, calls create_comment() using Actor instance, 
    calls publish_comment() using return create_comment()"""
    pass