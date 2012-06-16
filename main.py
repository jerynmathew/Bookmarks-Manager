from flask import Flask, render_template, flash, request
import os
import model

app = Flask(__name__)
app.debug = True # Remove before deploying
app.secret_key = os.urandom(32) # Need this for flash messages
    
'''
Main Page of Web App
'''
@app.route('/', methods=['GET', 'POST'])
def bookmarks():
    # By default, display the Entire table
    render_table = model.getBookmarks()
    # POST METHOD handling
    if request.method == 'POST':
        #Adding new bookmarks, and display complete (new) table
        if "textLink" in request.form.keys():
            model.addBookmark( Title=request.form["textTitle"],
                               Link=request.form["textLink"],
                               Tags=request.form["textTags"] )
            
            render_table = model.getBookmarks()
        #Search Request. Display only seacrhed entries!!
        elif "search" in request.form.keys():
            render_table = model.searchBookmarks( request.form["search"] )
            # In the event u searched for a non-existent tag 
            if len( render_table ) == 0:
                flash("No entries with the tag \'" + request.form["search"] + "\'")
    
    # Default GET METHOD Handling    
    return render_template( 'index.html', table=render_table, headers=['Title', 'Url', 'Tags'] )

    
# MAIN APPLICATION CODE
if __name__ == '__main__':
    app.run('127.0.0.1')    # Run in localhost:5000