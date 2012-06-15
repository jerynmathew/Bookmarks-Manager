from flask import Flask, render_template, flash, request
import re, os

app = Flask(__name__)
app.debug = True # Remove before deploying
app.secret_key = os.urandom(32) # Need this for flash messages

BookmarksList = [] #Replace with actual sqlite DB
    
'''
Main Page of Web App
'''
@app.route('/', methods=['GET', 'POST'])
def bookmarks():
    global BookmarksList
    #By default, display the Entire table
    render_table = BookmarksList
    
    # POST METHOD handling
    if request.method == 'POST':
        #Adding new bookmarks, and display complete (new) table
        if "textLink" in request.form.keys():
            addNewBookmark()
        #Search Request. Display only seacrhed entries!!
        elif "search" in request.form.keys():
            render_table = searchTags(request.form["search"])
            # In the event u searched for a non-existent tag 
            if len( render_table ) == 0:
                flash("No entries with the tag \'" + request.form["search"] + "\'")
    
    # Default GET METHOD Handling    
    return render_template( 'index.html', table=render_table, headers=['Title', 'Url', 'Tags'] )
    

'''
Adds New Bookmark to the global list.
TODO: Add entry into SQLite DB.
'''    
def addNewBookmark():
    Bookmark = {}
    
    Bookmark["Title"] = request.form["textTitle"]
    if request.form["textLink"].startswith( "http://") is False:
        Bookmark["Link"]  = "http://" + request.form["textLink"]
    else:
        Bookmark["Link"]  = request.form["textLink"]
    Bookmark["Tags"]  = re.findall( r'\w+', request.form["textTags"] )
    
    global BookmarksList
    BookmarksList.append( Bookmark )
    
'''
Search for tag
'''    
def searchTags( searchstring ):
    table = []
    global BookmarksList
    for entry in BookmarksList:
        print entry
        if searchstring.lower() in [x.lower() for x in entry["Tags"]]:
            table.append( entry )
    return table

    
# MAIN APPLICATION CODE
if __name__ == '__main__':
    app.run('127.0.0.1')    # Run in localhost:5000