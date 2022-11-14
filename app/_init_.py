# Jelly Jam Pancakes - Jeremy Kwok, Jacob Guo, Prattay Dey
# SoftDev
# 2022-11-07
# time spent: 

from flask import Flask            #facilitate flask webserving
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
        return render_template('feed.html', username = session['username'], method = request.method)
    return redirect(url_for('redirect_login'))

# REGISTER

# register
@app.route("/register", methods=['GET', 'POST'])
def register():
    # breakdown into GET and POST methods

    #GET
    if request.method == 'GET':
        input_username = request.args['username']
        input_password = request.args['password']

        username_check = f"select username from accounts where username='{input_username}';"

        c.execute(username_check)
        # if there isn't an account associated with said username then create one
        if not c.fetchone():
            c.execute("insert into accounts values(?, ?)", (input_username, input_password))
            return redirect(url_for('index'))
        # if username is already taken
        return render_template('register.html', message = "Username is already taken. Please select another username.")

    #POST
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        username_check = f"select username from accounts where username='{input_username}';"

        c.execute(username_check)
        # if there isn't an account associated with said username then create one
        if not c.fetchone():
            c.execute("insert into accounts values(?, ?)", (input_username, input_password))
        # if username is already taken
        return render_template('register.html', message = "Username is already taken. Please select another username.")

# redirect to user registration page
@app.route("/user_registration", methods=['GET', 'POST'])
def redirect_register():
    return render_template('register.html')

# LOGIN

# if user doesn't already have a session then prompt login
@app.route("/login", methods=['GET', 'POST'])
def redirect_login():
    print(session)
    return render_template('login.html')

# authorize
@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    # checks to see if the user enters a valid login, and creates a new session if so
    if request.method == 'GET':
        input_username = request.args['username']
        input_password = request.args['password']

        # Searchs accounts table for user-password combination
        login_check = f"select username from accounts where username='{input_username}' and password = '{input_password}';"
        username_check = f"select username from accounts where username='{input_username}';"
        password_check = f"select username from accounts where password='{input_password}';"

        c.execute(login_check)
        if c.fetchone():
            print("Login success!")
            session['username'] = request.args['username'] # stores username in session
            return render_template('feed.html', username = request.args['username'], password = request.args['password'], method = request.method)  #For 'get'

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


    # same thing, just adjusted for POST requests
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
            session['username'] = request.form['username'] # stores username in session
            return render_template('feed.html', username = request.form['username'], password = request.form['password'], method = request.method)  #For 'post'

        else:
            print("Login failed")
            error_msg = ''
            
            # Username check
            c.execute(username_check)
            if not c.fetchone():
                error_msg += "Username is incorrect. \n"
            
            #Password check
            c.execute(password_check)
            if not c.fetchone():
                error_msg += "Password is incorrect. \n"

            error_msg += "Please try again."
            return render_template('login.html', message = error_msg)

# logout and redirect to login page
@app.route("/logout", methods=['GET', 'POST'])
def redirect_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# create a story
@app.route("/redirect_create", methods=['GET', 'POST'])
def redirect_create():
    return render_template('create.html', message = "")

@app.route("/create", methods=['GET', 'POST'])
def create():

    username = session['username']
    
    #GET
    if request.method == 'GET':
        #storyID = 
        storyTitle = request.args['storyTitle']
        storyContent = request.args['storyContent']
        date = datetime.datetime.now().strftime("%y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        print(storyTitle)
        print(storyContent)

        title_check = f"select storyTitle from stories where storyTitle='{storyTitle}';"

        c.execute(title_check)
        # if there isn't an story associated with said title then create one
        if not c.fetchone():
            c.execute("insert into stories values(?, ?, ?, ?, ?)", (storyTitle, storyContent, username, date, time))
            return redirect(url_for('redirect_feed'))
        # if storyTitle is already taken
        return render_template('create.html', message = "Story Title is already taken. Please select another Title.")

    #POST
    if request.method == 'POST':
        #storyID = 
        storyTitle = request.form['storyTitle']
        storyContent = request.form['storyContent']
        date = datetime.datetime.now().strftime("%y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        print(storyTitle)
        print(storyContent)

        title_check = f"select storyTitle from stories where storyTitle='{storyTitle}';"

        c.execute(title_check)
        # if there isn't an story associated with said title then create one
        if not c.fetchone():
            c.execute("insert into stories values(?, ?, ?, ?, ?)", (storyTitle, storyContent, username, date, time))
            return redirect(url_for('redirect_feed'))
        # if storyTitle is already taken
        return render_template('create.html', message = "Story Title is already taken. Please select another Title.")

@app.route("/redirect_feed", methods=['GET', 'POST'])
def redirect_feed():
    return render_template('feed.html', message = "")

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