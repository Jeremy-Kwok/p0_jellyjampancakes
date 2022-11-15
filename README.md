# P00 by Jelly-Jam-Pancakes
## Roster:
- Devo Jeremy (PM) - SQL
- Devo Prattay - Flask
- Devo Jacob - HTML/CSS

## Description of Website/App:
under construction...

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

    SQLite3:
        -Tables can be sorted in an ASC and DESC order:
        https://www.sqlitetutorial.net/sqlite-order-by/

        -To get only n row(s) from a select command, use limit n
        -Insert into [tableName] select... allows you to insert a row from another table into [tableName]

        -To update an entire column at once use "update [tableName] set [columnName]='_____'"
        https://www.sqlitetutorial.net/sqlite-update/ 

        -"select distinct [columnName]" allows you to avoid selecting rows with duplicate values in a [columnName]

    Python-Flask:
        -redirect(url_for('[page path]')) redirects user to that page

        -datetime.datetime.now() allows you to get the date and time in the specified format (%y = year, %m = month, %d = day, %H = hour, %M = minute, %S = second)

        -

    HTML:
    
### QCC:
    Why does the website sometimes render "Access to 127.0.0.1 was denied" when we run it? But then it goes on to work in an incognito window.

    



#
only need a working database, nothing in it