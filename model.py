import json
import re

JSON_FILE = r".\static\bookmarks.json"

'''
Fetches bookmarks table
'''
def getBookmarks():
    fp = open( JSON_FILE, 'r' )
    table = json.load( fp )
    fp.close()
    return table

'''
Search Table of Bookmarks for specific tag
'''
def searchBookmarks( searchstring ):
    table = []
    fulltable = getBookmarks()
    for entry in fulltable:
        if searchstring.lower() in [ x.lower() for x in entry["Tags"] ]:
            table.append( entry )
    return table
    
'''
Add new bookmark to file
'''
def addBookmark( **bookmark ):
    table = getBookmarks()
    
    if bookmark["Link"].startswith( "http://") is False:
        bookmark["Link"] = "http://" + bookmark["Link"]
    bookmark["Tags"] = re.findall( r'\w+', bookmark["Tags"] )
        
    table.append( bookmark )
    
    fp = open( JSON_FILE, 'w' )
    json.dump( table, fp )
    fp.close()
    