# P00 by Jelly-Jam-Pancakes
## Roster:
- Devo Jeremy (PM) - SQL
- Devo Prattay - Flask
- Devo Jacob - HTML/CSS

## Description of Website/App:
- Our website can create and hold user-generated stories.
- A new user must first register an account and then go back to the login portal.
- Users must be logged in to view/edit/create stories.
- After login, users will land on the feed page. There is two options from here: Create a new story OR View existing ones
- The create page will have two fields that must be filled out to create a new story: story title and story content
- The library page displays all the stories a user has previously edited, as well as an option to explore new stories.
- A user cannot edit the same story multiple times.

## Launch codes:
Clone the repo into your local machine
```
git clone git@github.com:Jeremy-Kwok/p0_jellyjampancakes.git
```
Move into the right directory
```
cd p0_jellyjampancakes/app/
```
Run this python file to start serving Flask app
```
python3 _init_.py
```
A line such as below will appear in your terminal. Copy and paste the given URL into the browser to load the landing page
```
* Running on http://127.0.0.1:5000
```


### DISCO:

    check_same_thread: https://www.folkstalk.com/2022/09/sqlite3-programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-same-thread-with-code-examples.html

    Python-Flask:
        - os.urandom(num) will generate a String of size num bytes -- useful for private session keys

        -redirect(url_for('[page path]')) redirects user to that page

        -datetime.datetime.now() allows you to get the date and time in the specified format (%y = year, %m = month, %d = day, %H = hour, %M = minute, %S = second)

    HTML:
        - For the input type submit, it's useful to use the 'value' attribute to change from the default value of "Submit" or "Submit Query" to something more specific such as "Create Story" or "Login"

### QCC:
    Why does the website sometimes render "Access to 127.0.0.1 was denied" when we run it? But then it goes on to work in an incognito window.




#
only need a working database, nothing in it
