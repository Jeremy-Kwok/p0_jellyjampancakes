# Jelly Jam Pancakes - Jeremy Kwok, Jacob Guo, Prattay Dey
# SoftDev
# 2022-11-07
# time spent: 

#Username: Pancake
#Password: Syrup

from flask import Flask            #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #facilitate user sessions
from flask import redirect, url_for #to redirect to a different URL
import os

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #randomized string for key


required_username = "Pancake"
required_password = "Syrup"

# checks to see if the user already has a session
@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template('response.html', username = session['username'], method = request.method)
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    print(session)
    return render_template('login.html')


@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    # checks to see if the user enters a valid login, and creates a new session if so
    if request.method == 'GET':
        input_username = request.args['username']
        input_password = request.args['password']

        if input_username == required_username and input_password == required_password:
            session['username'] = request.args['username'] # stores username in session
            return render_template('response.html', username = request.args['username'], password = request.args['password'], method = request.method)  #For 'get'

        else:
            error_msg = ''
            if input_username != required_username:
                error_msg += "Username is incorrect. \n"
            if input_password != required_password:
                error_msg += "Password is incorrect. \n"
            error_msg += "Please try again."
            return render_template('login.html', message = error_msg)


    # same thing, just adjusted for POST requests
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        if input_username == required_username and input_password == required_password:
            session['username'] = request.form['username'] # stores username in session
            return render_template('response.html', username = request.form['username'], password = request.form['password'], method = request.method)  #For 'post'

        else:
            error_msg = ""
            if input_username != required_username:
                error_msg += "Username is incorrect. \n"
            if input_password != required_password:
                error_msg += "Password is incorrect. \n"
            error_msg += "Please try again."
            return render_template('login.html', message = error_msg)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
