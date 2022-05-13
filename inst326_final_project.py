"""A program that looks through posts on the subreddit r/movies and comments information about an actor if they are mentioned in the post title.
Group Members: McKenna Shay, Declan Dmitriev, Chikezie Okoli, Surafel Assres
Assignment: INST326 Final Project
Date: 4_14_22
Challenges Encountered: learning about the APIs we are using, figuring out how to find an actor's name in a title, 
getting an actor's most popular movies (stored in their "known for" list of IMDB), getting awards won by an actor
"""
import csv
from imdb import Cinemagoer
import datetime
import praw
import re
import requests
from bs4 import BeautifulSoup
import string

class Actor:
    """Captures and holds information about an actor using an IMDB page.
    
    Attributes:
        name (str): full name of actor
        age (int/str): current age of actor or age at passing if actor has died (as a str)
        dob (str): date of birth of actor
        pob (str): place actor was born
        works (list of strings): 4 of the actor's most popular movies/shows with title & year released
        awards (list of strings): 3-4 of some of the awards the actor has won
    """
    def __init__(self, actor_id):
        """Sets the attributes for the Actor.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Raises:
            TypeError: a Cinemagoer actor object does not have a birth place
            
        Side Effects:
            Sets name, age, dob, pob, works, and awards attributes
        """
        imdb = Cinemagoer()

        # gets actor's Cinemagoer object
        actor = imdb.get_person(actor_id)
        self.name = actor.get('name')
        
        birthday = actor.get('birth date')
            
        # creates a deatetime object of actor's birthday
        birthday_list = birthday.split('-')
        birthdate = datetime.date(int(birthday_list[0]), int(birthday_list[1]), int(birthday_list[2]))
        
        # checks if an actor has died and sets self.age as their age at their death if they did
        deathday = actor.get('death date')
        if deathday:
            death_date_list = deathday.split('-')
            death_date = datetime.date(int(death_date_list[0]), int(death_date_list[1]), int(death_date_list[2]))
        
            self.age = death_date.year - birthdate.year - ((death_date.month, death_date.day) < (birthdate.month, birthdate.day))
            self.age = str(self.age) + " (at passing)"
        # if the actor has not died, sets self.age to current age using today's date
        else:
            today = datetime.date.today()
            self.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    
        # formats actor's birthday for self.dob
        datetime_birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        self.dob = datetime_birthday.strftime('%B %d, %Y')
        
        # checks if Cinemagoer has the actor's place of birth and sets self.pob to it if so
        try:
            self.pob = actor.get('birth info')['birth place']
        except TypeError:
            self.pob = 'Could not find one'
        
        # sets self.works and self.awards using the functions to determine them
        self.get_popular_movies(actor_id)
        self.get_actor_awards(actor_id)

    def get_popular_movies(self, actor_id):
        """Gets 4 of the most popular movies with the actor using a TSV file.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Side Effects:
            Sets works attribute
        """
        imdb = Cinemagoer()
        
        self.works = []
        known_for = []

        # opens data.tsv file and gets the row for the actor
        target_row = open_tsv_file('nm'+actor_id, 0)
        # gets actor's "known for" list that stores their 4 most popular movies
        known_for = target_row[5].split(',')

        # gets movie code for each movie in the actor's "known for" list
        count = 0
        for film in known_for:
            movie_code = film[2:]
            known_for[count] = imdb.get_movie(movie_code)
            count+=1

        # adds each movie in actor's "known for" list to self.works with its title & year released
        for work in known_for:
            self.works.append(f"{work.data['title']} ({work.data['year']})")
                
    
    def get_actor_awards(self, actor_id):
        """Gets 3-4 of the most recent awards the actor won using web scraping.
        
        Args:
            actor_id (int): the IMDB id of the actor
            
        Raises:
            AttributeError: going through the HTML for the awards webpage on IMDB does not have a b or contents attribute.
            
        Side Effects:
            Sets awards attribute
        """
        # gets url of actor's IMDB awards page & requests access to it using BeautifulSoup
        actor_awards_page = f"https://www.imdb.com/name/nm{actor_id}/awards?ref_=nm_awd"
        request_page = requests.get(actor_awards_page)
        soup = BeautifulSoup(request_page.text, "html.parser")
        # gets all awards that are stored between <tr> </tr>
        all_awards = soup.find_all("tr")

        awards_won = []
        # checks if the actor won the award being examied and adds it to awards_won if so
        for award in all_awards:
            try:
                award_outcome = award.b.contents[0]
                if award_outcome == "Winner":
                    awards_won.append(award)
            except AttributeError:
                continue
        
        self.awards = []
        for count, award in enumerate(awards_won):
            # finds the full HTML of the current award being looked at
            award_html = award.find_all("td")

            # uses regex to find the award's year and sets award_year equal to it if it exists
            award_year = re.findall(r"> (\d{4})", str(award_html[0].contents[1]))
            if award_year:
                award_year = award_year[0]
            
            # uses regex to find the award category and sets award_category equal to it if it exists
            award_category = re.findall(r"\"award_category\">(.*)<", str(award_html[1].contents[4]))
            if award_category:
                award_category = award_category[0]
            
            # sets award_description equal to the description if the award if it stored in the HTML
            award_description = ''
            if len(award_html) > 2:
                award_description = award_html[2].contents[0].lstrip()
            
            # adds the award to self.awards if the award has a year, a category, and a description
            # avoids adding empty awards to the list
            if award_year and award_category and award_description:
                self.awards.append(str(award_year) + " " + str(award_category) + " for " + str(award_description))
               
            # once at most 4 awards are examined, the loop ends 
            if count > 3:
                break
    
def get_post(post):
    """Accesses each post in r/movies.
    
    Args:
        post (Reddit object): current Reddit post being examined
        
    Returns:
        a tuple with the title (str) and the ID number (int) of the Reddit post currently being looked at
    """
    return post.title, post.id

def find_actor(post_title, actor_names):
    """Looks for an actor's name in the title of a post using a csv file.
    
    Args:
        post_title (str): the title of the post being examined
        actor_names (list of str): a list of all actor names in data.tsv
        
    Returns:
        actor_page (int): the IMDB page ID of the actor's page taken from find_actor_page
    """
    # splits each word in the title into a list (only if words are divided by spaces)
    title = post_title.split(' ')
    title_pairs = []

    # creates a list where each element is every two words in the title that are next to each other
    first_word = title[0]
    for count, word in enumerate(title[1:]):
        # gets rid of "'s" from the end of the word
        # used if the post title refers to an actor using  a possessive
        if word[-2:] == "'s":
            word = word.replace(word, word[0:-2])
            
        # strips word of punctuation at the end of the word
        # used if an actor's name is mentioned with punctuation so it can still be matched
        word = word.replace(word, word.strip(string.punctuation))
        
        # adds the pairs of words in the post title to the list
        if count == 0:
            title_pairs.append(first_word + ' ' + word)
        else:
            title_pairs.append(title[count] + ' ' + word)
    
    actor_name = ''
    actor_page = ''
    
    # uses the pairs of words in the title previously found to match with a potential actor's name identified in the post
    # title_pair has to match name from actor_names list exactly (with punctuation and capitalization)
    for title_pair in title_pairs:
        if title_pair in actor_names:
            actor_name = title_pair
            # tries to find an actor's IMDB page with the match found
            actor_page = find_actor_page(actor_name)
            
            # if an actor's name was found the loop breaks, else it continues
            if actor_page != None:
                break
            
            actor_name = ''
    
    # if an actor's name was found the actor's IMDB page ID is returned else None is returned
    if actor_name != '':
        return actor_page
    
    return None

def find_actor_page(actor_name):
    """Looks through IMDB for the actor's page.
    
    Args:
        actor_name (str): the name of the actor
        
    Returns: 
        page_id (int): the IMDB page id of the actor's page
    """ 
    # gets the row in data.tsv with the match's name
    target_row = open_tsv_file(actor_name, 1)
    
    if target_row != None:
        # gets a list of the match's professions from the data.tsv row
        profession = target_row[4].split(',')
    
        # if actor/actress is one of the match's professions and if the match has a year of birth stored the page_id of the actor is returned
        # year of birth is checked because data.tsv stores some characters' information as actors
        if ('actor' in profession or 'actress' in profession) and target_row[2] != '\\N':
            # substrings off the "nm" from the page ID so it is just an int
            page_id = target_row[0]
            return page_id[2:]
    
    return None

def create_comment(actor, actor_id):
    """Creates a string comment with an Actor object's attributes.
    
    Args:
        actor (Actor): the actor the comment is about
        actor_id (int): the IMDB page ID of the actor
        
    Returns:
        comment (str): hold all the info about the actor parameter
    """
    # formats strings according to Reddit's formatting for the actor's name, age, dob, & pob
    actor_name = f"**Actor's Name:** {actor.name}    "
    actor_age = f"**Actor's Age:** {actor.age}    "
    actor_dob = f"**Actor's Date of Birth:** {actor.dob}    "
    actor_pob = f"**Actor's Place of Birth:** {actor.pob}    "

    # formats a list to comment the actor's popular works
    actor_works_comment = "**Popular Works:**    "
    for count, work in enumerate(actor.works):
        actor_works_comment += f"""    
            {count+1}. {work}"""
    
    # formats a list to comment some of the actor's award won
    actor_awards_comment = "**Some Awards Won:**    "
    # if the program found awards for the actor on their IMDB awards page the list is added to the comment, else "Could not find any" is added
    if actor.awards:
        for count, award in enumerate(actor.awards):
            actor_awards_comment += f"""    
            {count+1}. {award}"""
    else:
        actor_awards_comment += " Could not find any    "
        
    # creates a mistakes message and gives the link to the actor's IMDB page
    mistakes_message = f"""This bot gives information about the first actor mentioned in a post title on r/movies, but sometimes mistakes are made. 
Click [here](https://www.imdb.com/name/nm{actor_id}/) to learn more about the actor found for this post!"""
    
    # returns a fully formatted comment to post on Reddit
    return (actor_name + """ 
""" + actor_age + """ 
""" + actor_dob + """ 
""" + actor_pob + """ 
""" + actor_works_comment + """    
""" + actor_awards_comment + """ 
 
""" + mistakes_message)

def publish_comment(post, comment):
    """Comments a string to a Reddit post.
    
    Args:
        post (Reddit object): the post that has the actor's name in it
        comment (str): the comment that will be published to the post
    """
    post.reply(comment)

def open_tsv_file(target, row_num):
    """Opens data.tsv files and tries to find a target within the files.
    
    Args:
        target (int/str): what is trying to be found within data.tsv
        rwo_num (int): the column of the TSV file that might hold the target
        
    Returns:
        the row as a list that the target is found on in the data.tsv file
    """
    tsv_file=open('data1.tsv', mode='r', encoding='utf8')
    read_tsv=csv.reader(tsv_file,delimiter="\t")
    
    filename = 2
    
    # goes through each row in each data.tsv file and checks if it holds the target
    while True:
        # checks current tsv_file for target
        for line in tsv_file:
            for row in read_tsv:
                if row[row_num] == target:
                    tsv_file.close()
                    return row
            
        # once one data.tsv file reaches its end, tsv_file gets reset to the next data.tsv file   
        tsv_file = open('data'+str(filename)+'.tsv', mode='r', encoding='utf-8')
        filename += 1
        
        if filename > 9:
            tsv_file.close()
            break
        
def get_imdb_actor_names():
    """Gets all actor names in the data.tsv files.
    
    Returns:
        a list of strings with all the actor names found
    """
    actor_names=[]
    
    tsv_file = open("data1.tsv", mode='r', encoding='utf8')
    read_tsv = csv.reader(tsv_file,delimiter="\t")
          
    filename = 2
    
    # goes through each row in data.tsv and adds the name column to actor_names 
    while True:
        # adds actor names from current data.tsv file
        for line in tsv_file:
            for row in read_tsv:
                actor_names.append(row[1])
                
        # once end of a data.tsv file is reached, resets tsv_file to the next data.tsv file
        tsv_file = open('data'+str(filename)+'.tsv', mode='r', encoding='utf-8')
        filename += 1
        
        if filename > 9:
            break
    
    tsv_file.close()
    
    return actor_names

def main():
    """Runs the entire program by combining all the functions together.
    
    Side Effects:
        prints the Reddit post title, post ID, actor's IMDB page ID, comment if created, and a message that the comment was published to Reddit to the terminal
    """
    # gets access to reddit
    reddit = praw.Reddit(
        client_id = "_0kHj0UNHLgsztUOBVIYXg",
        client_secret = "dgjr6dsvP1CXB_N1jzN5ng08rUQEQw",
        user_agent = "<platform>:<app ID>:<version string> (by u/INSTbot)",
        username = "INSTbot",
        password = "inst326project",
    )
    
    # gets acotr_names list and access to r/movies
    actor_names = get_imdb_actor_names()
    movies_sub = reddit.subreddit("movies")
    
    # goes through the 5 newest submissions on r/movies
    for count, submission in enumerate(movies_sub.new(limit=5)):
        # gets the post title & ID and prints it to the terminal
        post_title, post_id = get_post(submission)
        print(f"\n\033[1mPost #{count+1} Title:\033[0m \"{post_title}\" \t \033[1mPost ID:\033[0m {post_id}")
        # determines if there is an actor mentioned in the title and gets their IMDB page ID if so
        actor_page = find_actor(post_title, actor_names)
        # prints the actor's ID to the terminal, prints None if no actor was found
        print(f"\033[1mActor IMDB Page ID:\033[0m {actor_page}")
   
        # if an actor was found, creates an Actor object based off actor found and a comment, posts it to reddit 
        if actor_page != None:
            actor = Actor(actor_page)
            
            comment = create_comment(actor, actor_page)
            print('\n\033[1mPost Comment:\033[0m \n"' + comment + '"')
            publish_comment(submission, comment)
            print('\nPublished comment! Check Reddit post for comment.')

if __name__ == "__main__":
    # calls main to run program
    main()