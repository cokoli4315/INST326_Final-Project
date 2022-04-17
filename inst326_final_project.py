"""A program that looks through posts on the subreddit r/movies and comments information about an actor if they are mentioned.

Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project
Date: 4_14_22
Challenges Encountered: 
"""
from imdb.Person import Person
from imdb import Cinemagoer
import praw

class Actor:
    """Captures and holds information about an actor using an IMDB page.
    
    Attributes:
        name (str): full name of  actor
        age (int): current age of actor
        dob (str): date of birth of actor
        pob (str): place actor was born
        movies (list): 3-5 of the actor's most populat movies with title & year released
        awards (list): 3-5 of the actor's most recent awards
    """

    def __init__(self, actor_id):
        """Sets the attributes for the Actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Side Effects:
            Sets name, age, dob, pob, movies, and awards attributes
        """
        pass
    
    def get_popular_movies(self, actor_id):
        """Gets 3-5 of the most popular movies with the actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
        """
        pass
    
    def get_recent_awards(self, actor_id):
        """gets 3-5 of the most recent awards the actor won.
        
        Args:
            actor_id (int): the IMDB id of the actor
        """
        pass
    
def get_post(subreddit):
    """Accesses each post in r/movies.
    
    Args:
        subreddit: the subreddit we are looking through
        
    Returns:
        post_id (int): the ID number of the Reddit post currently being looked at
    """
    #get access to r/movies, fix for final
    movies_sub = reddit.subreddit("movies")
    #goes through 10 most recent posts on r/movies and prints info about them, not in final just an example
    for submission in movies_sub.new(limit=10):
        print(submission.title)
        print(submission.score)
        print(submission.id) # return this, fix for final
        print(submission.url)

def get_title(post_id):
    """Accesses the title of each post. 
    
    Args:
        post_id (int): the ID of the post being examined.
        
    Returns:
        post_title (str): the title of the post
    """
    return post_id.title
        
def find_actor_name(post_title):
    """Looks for an actor's name in the title of a post using regex.
    
    Args:
        post_title (str): the title of the post being examined
        
    Returns:
        actor_name (str): the name of the actor if found
    """
    pass

def find_actor_page(actor_name):
    """Looks through IMDB for the actor's page.
    
    Args:
        actor_name (str): the name of the actor
        
    Returns: 
        page_id (int): the IMDB page id of the actor's page
    """
    pass

def create_comment(actor):
    """Creates a string comment with an Actor object's attributes.
    
    Args:
        actor (Actor): the actor the comment is about
        
    Returns:
        comment (str): hold all the info about the actor parameter
    """
    pass

def publish_comment(post_id, comment):
    """Comments a string to a Reddit post.
    
    Args:
        post_id (int): the ID of the post that has the actor's name in it
        comment (str): the comment that will be published to the post
    """
    pass

def main():
    """Runs the entire program. Calls get_posts(), calls get_title() for each post, calls find_actor_name() for title, 
    if an actor's name is found calls find_actor_page(), if a page for the actor is found creates an Actor instance, 
    calls create_comment() using the Actor instance, calls publish_comment() using the return of create_comment()"""
    # gets access to reddit, just an example not in final
    reddit = praw.Reddit(
        client_id="my client id",
        client_secret="my client secret",
        user_agent="my user agent",
        username="my username",
        password="my password",
    )

if __name__ == "__main__":
    # calls main to run program
    main()