**One to four sentences explaining what your project is and what it does.**

The concept of this project is to create a Reddit bot that searches through posts on r/movies and comments information about an actor. The bot collects information from IMDB about different actors using matches from Reddit. 
 
**An explanation on how to run the program from the command line.**

Running from the command line is simple, there are no arguments added. Just run “python inst326_final_project.py” for Windows or “python3 inst326_final_project.py” for Mac. Make sure BeautifulSoup, Cinemagoer, and PRAW are all downloaded (using pip) on the machine running the program. Additionally, all 9 of the data.tsv files should be in the same directory as the program. 

**Documentation on how to use the program / how to interpret the output of the program.**
There is not any input required to run the program, all the work is done within the program. Everything in the output is labelled, you can see the post title and ID, the actor’s IMDB ID (if it says None then an actor was not found in the post title and a comment is not made or posted), the comment that should be published to Reddit and a line that says to check Reddit for comment. Then you can go to r/movies on Reddit (here is a link), make sure it is sorted by new, and check the 5 most recent posts for comments. 

**An annotated bibliography of all sources you used to develop the program and how you used them.**

Cruz, G. (2022). Web Scraping [Slides]. Panopto. https://umd.instructure.com/courses/1320811/modules/items/11297694
	This source was used to better understand web scraping for the get_actor_awards() method. This source helped guide our use of BeautifulSoup and understanding of HTML for the purposes of uor web scraping needs. 

PRAW: The Python Reddit API Wrapper — PRAW 7.6.0 documentation. (n.d.). Read the Docs. https://praw.readthedocs.io/en/stable/
	This is the documentation for the Reddit API, which we used a lot in our code. We used this source to better understand how to use Praw and be able to access a current instance of Reddit, search through posts in r/movies, get information about posts easily, and easily post comments to Reddit.

Python Dates. (n.d.). W3Schools. https://www.w3schools.com/python/python_datetime.asp
	This source was used to better understand the datetime module that was used in our code. It was used to determine the age of an actor, either by using today’s date or the date of their death. Additionally, it was used to reformat the birthday that is stored in Cinemagoer to look more like a string for the Reddit comment. 
	
	Quick start — Cinemagoer 6.8 documentation. (n.d.). Read the Docs. https://cinemagoer.readthedocs.io/en/latest/usage/quickstart.html 
	This is the documentation for the IMDB API, which we used extensively. This was used to learn how to gain information on an actor, such as their IMDB page ID, and their basic information (such as name, date of birth, and place of birth). This is what the Actor __init__ uses to set the Actor class attributes.
