# Jelly Jam Pancakes - Jeremy Kwok, Jacob Guo, Prattay Dey
# SoftDev
# 2022-11-07
# time spent: 

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #facilitate user sessions
from flask import redirect, url_for #to redirect to a different URL
import os
import datetime                     #tell time

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #randomized string for SECRET KEY (for interacting with operating system)

import sqlite3

DB_FILE="tables.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("create table if not exists accounts(username text, password text);")
c.execute("create table if not exists stories(storyTitle text, storyContent text, username text, date text, time text);")

# checks to see if the user already has a session
@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template('feed.html', username = session['username'])
    return redirect(url_for('redirect_login'))

# REGISTER

# register
@app.route("/register", methods=['GET', 'POST'])
def register():

    input_username = ""
    input_password = ""
    input_confirm_password = ""

    # breakdown into GET and POST methods

    #GET
    if request.method == 'GET':
        input_username = request.args['username']
        input_password = request.args['password']
        input_confirm_password = request.args['confirm password']

    #POST
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']
        input_confirm_password = request.form['confirm password']

    #Checks for password/confirm password match
    if input_password != input_confirm_password:
        return render_template('register.html', message = "Passwords do not match. Please try again.")

    #Checks for existing username in accounts table
    c.execute(f"select username from accounts where username='{input_username}';")
    
    # if there isn't an account associated with said username then create one
    if not c.fetchone():
        c.execute("insert into accounts values(?, ?)", (input_username, input_password))
        return render_template('login.html')
    # if username is already taken
    else:
        return render_template('register.html', message = "Username is already taken. Please select another username.")

# redirect to user registration page
@app.route("/redirect_register", methods=['GET', 'POST'])
def redirect_register():
    return render_template('register.html')

# LOGIN

# login process
@app.route("/login", methods=['GET', 'POST'])
def login():

    # GET
    if request.method == 'GET':
        input_username = request.args['username']
        input_password = request.args['password']

    # POST
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

    # Searchs accounts table for user-password combination
    login_check = f"select username from accounts where username='{input_username}' and password = '{input_password}';"
    username_check = f"select username from accounts where username='{input_username}';"
    password_check = f"select username from accounts where password='{input_password}';"

    c.execute(login_check)
    if c.fetchone():
        print("Login success!")
        if request.method == 'GET': #For 'get'
            session['username'] = request.args['username'] # stores username in session 

        if request.method == 'POST': #For 'post'
            session['username'] = request.form['username'] # stores username in session 
        
        return render_template('feed.html', username = session['username'])

    else:
        print("Login failed")
        error_msg = ''
            
        # Username check
        c.execute(username_check)
        if not c.fetchone():
            error_msg += "Username is incorrect or not found. \n"
        
        #Password check
        c.execute(password_check)
        if not c.fetchone():
            error_msg += "Password is incorrect or not found. \n"

        error_msg += "Please try again."
        return render_template('login.html', message = error_msg)

# if user doesn't already have a session then prompt login
@app.route("/redirect_login", methods=['GET', 'POST'])
def redirect_login():
    print(session)
    return render_template('login.html')

# logout and redirect to login page
@app.route("/logout", methods=['GET', 'POST'])
def redirect_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# FEED

@app.route("/redirect_feed", methods=['GET', 'POST'])
def redirect_feed():
    return render_template('feed.html', username = session['username'], message = "")

@app.route("/create", methods=['GET', 'POST'])
def create():

    username = session['username']
    date = datetime.datetime.now().strftime("%y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")
    
    #GET
    if request.method == 'GET':
        #storyID = 
        storyTitle = request.args['storyTitle']
        storyContent = request.args['storyContent']

    #POST
    if request.method == 'POST':
        #storyID = 
        storyTitle = request.form['storyTitle']
        storyContent = request.form['storyContent']

    print("Story Title: " + storyTitle)
    print("Story Content: " + storyContent)

    c.execute(f"select storyTitle from stories where storyTitle='{storyTitle}';")

    # if there isn't an story associated with said title then create one
    if not c.fetchone():
        c.execute("insert into stories values(?, ?, ?, ?, ?)", (storyTitle, storyContent, username, date, time))
        print("Publish Success!")
        return redirect(url_for('redirect_feed'))

    # if storyTitle is already taken
    print("Publish fail: Title already taken")
    return render_template('create.html', message = "Story Title is already taken. Please select another Title.")

@app.route("/redirect_create", methods=['GET', 'POST'])
def redirect_create():
    return render_template('create.html', message = "")

@app.route("/library", methods=['GET', 'POST'])
def library():

    username = session['username']

    # deletes old recentFeed table and creates a new one
    c.execute("drop table recentFeed;")
    c.execute("create table if not exists recentFeed(storyTitle text, storyContent text, username text, date text, time text, userEdit int);")

    # FOR STORIES THE USER HAS ALREADY EDITED

    # takes all unique titles in stories table that the username has edited
    c.execute(f"select distinct storyTitle from stories where username='{username}';")
    editedTitles = c.fetchall()

    # for each storyTitle:
    # 1. sorts entries with most recent at the top, 
    # 2. selects the most recently edited story record 
    # 3. inputs it into recentFeed
    for rows in editedTitles:
        c.execute(f"insert into recentFeed select * from stories where storyTitle='{rows}' order by date DESC, time DESC limit 1;")

    # for all added entries, input 1 to indicate the user has edited them already
    c.execute("update recentFeed set userEdited=1")
    
    # FOR STORIES THE USER HAS NOT EDITED

    # takes all unique titles in stories table that the username has NOT edited
    c.execute(f"select distinct storyTitle from stories where username!='{username}';")
    uneditedTitles = c.fetchall()

    # for each storyTitle:
    # 1. sorts all entries with most recent at the top, 
    # 2. selects the most recently edited story record 
    # 3. inputs it into recentFeed
    for rows in editedTitles:
        c.execute(f"insert into recentFeed select * from stories where storyTitle='{rows}' order by date DESC, time DESC limit 1;")

    # for all newly added entries, input 0 to indicate the user has NOT edited them yet
    c.execute("update recentFeed set userEdited=0 where userEdited!=1")

    # send everything in recentEdited to library.html
    c.execute("select * from recentFeed")
    results = c.fetchall()
    return render_template("library.html", feed = results)


@app.route("/redirect_library", methods=['GET', 'POST'])
def redirect_library():
    
    username = session['username']

    # deletes old recentFeed table and creates a new one
    c.execute("drop table recentFeed;")
    c.execute("create table if not exists recentFeed(storyTitle text, storyContent text, username text, date text, time text, userEdited int);")

    # FOR STORIES THE USER HAS ALREADY EDITED

    # takes all unique titles in stories table that the username has edited
    c.execute(f"select distinct storyTitle from stories where username='{username}';")
    editedTitles = c.fetchall()
    print(editedTitles)

    # for each storyTitle:
    # 1. sorts entries with most recent at the top, 
    # 2. selects the most recently edited story record 
    # 3. inputs it into recentFeed
    for tupleTitles in editedTitles:
        titles = tupleTitles[0]
        print("Edited: " + titles)
        c.execute(f"insert into recentFeed (storyTitle, storyContent, username, date, time) select storyTitle, storyContent, username, date, time from stories where storyTitle='{titles}' order by date DESC, time DESC limit 1;")

    # for all added entries, input 1 to indicate the user has edited them already
    c.execute("update recentFeed set userEdited=1")
    
    # FOR STORIES THE USER HAS NOT EDITED

    # takes all unique titles in stories table that the username has NOT edited
    c.execute(f"select distinct storyTitle from stories where username!='{username}';")
    uneditedTitles = c.fetchall()

    # for each storyTitle:
    # 1. sorts all entries with most recent at the top, 
    # 2. selects the most recently edited story record 
    # 3. inputs it into recentFeed
    for tupleTitles in uneditedTitles:
        titles = tupleTitles[0]
        print("Unedited: " + titles)
        c.execute(f"insert into recentFeed select * from stories where storyTitle='{titles}' order by date DESC, time DESC limit 1;")

    # for all newly added entries, input 0 to indicate the user has NOT edited them yet
    c.execute("update recentFeed set userEdited=0 where userEdited!=1")

    # send everything in recentEdited to library.html
    c.execute("select * from recentFeed")
    results = c.fetchall()
    #print("Results: " + results)
    return render_template("library.html", feed = results)

@app.route('/view')
def view():

    #GET
    if request.method == 'GET':
        storyTitle = request.args['storyTitle']
        list = c.execute('select * from entries').fetchall()

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

db.commit() #save changes
db.close()  #close database