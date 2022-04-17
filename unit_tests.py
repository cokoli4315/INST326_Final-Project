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

import inst326_final_project as fp

def test_get_post():
    assert fp.get_post("movies") == #Nic Cage post id
    assert fp.get_post("movies") == #Blade Runner post id
    assert fp.get_post("movies") == #21 years post id
    assert fp.get_post("movies") == #Ryan Reynolds post id

def test_get_title():
    assert fp.get_title(post_id) == "Nicolas Cage Says He's Done His Best Work in the Last 10 Years"
    assert fp.get_title(post_id) == "Blade Runner (1982) Deckard never speaks to Roy, is there any other movie that never has the protagonist speak to the antagonist?"
    assert fp.get_title(post_id) == "21 years since Rat Race, Its time for another \"Big ensemble cast of actors chase around America for money\" movie"
    assert fp.get_title(post_id) == "Ryan Reynolds To Narrate Discovery+ Documentary 'Curb Your Carbon'"

def test_find_actor_name():
    assert fp.find_actor_name("Nicolas Cage Says He's Done His Best Work in the Last 10 Years") == "Nicolas Cage"
    assert fp.find_actor_name("Blade Runner (1982) Deckard never speaks to Roy, is there any other movie that never has the protagonist speak to the antagonist?") == None
    assert fp.find_actor_name("21 years since Rat Race, Its time for another \"Big ensemble cast of actors chase around America for money\" movie") == None
    assert fp.find_actor_name("Ryan Reynolds To Narrate Discovery+ Documentary 'Curb Your Carbon'") == "Ryan Reynolds"


def test_find_actor_page():
    assert fp.find_actor_page("Nicolas Cage") == 0000115
    assert fp.find_actor_page("Ryan Reynolds") == 0005351

def test_create_comment():
    nic_cage = fp.Actor(fp.find_actor_page("Nicolas Cage"))
    assert fp.create_comment(nic_cage) == "comment"
    ryan_reynolds = fp.Actor(fp.find_actor_page("Ryan Reynolds"))
    assert fp.create_comment(ryan_reynolds) == "comment"