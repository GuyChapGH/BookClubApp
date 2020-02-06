import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

from datetime import datetime

import pprint
import sys
from apiclient.discovery import build

# Store sensitive key in separate file
# from projectkey import API_KEY


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(query):
    """Look up query."""
#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# For this example, the API key is provided from projectkey file
    api_key = API_KEY

# The apiclient.discovery.build() function returns an instance of an API service
# object that can be used to make API calls. The object is constructed with
# methods specific to the books API. The arguments provided are:
#   name of the API ('books')
#   version of the API you are using ('v1')
#   API key
    service = build('books', 'v1', developerKey=api_key, cache_discovery=False)

# The books API has a volumes().list() method that is used to list books
# given search criteria. Arguments provided are:
#   volumes source ('public')
#   search query ('android')
# The method returns an apiclient.http.HttpRequest object that encapsulates
# all information needed to make the request, but it does not call the API.
    request = service.volumes().list(source='public', q=query)

# The execute() function on the HttpRequest object actually calls the API.
# It returns a Python object built from the JSON response. You can print this
# object or refer to the Books API documentation to determine its structure.
    response = request.execute()
# pprint.pprint(response)

# Accessing the response like a dict object with an 'items' key returns a list
# of item objects (books). The item object is a dict object with a 'volumeInfo'
# key. The volumeInfo object is a dict with keys 'title' and 'authors'.
# print 'Found %d books:' % len(response['items'])
# for book in response.get('items', []):
 # print (
#    book['volumeInfo']['title'],
#    book['volumeInfo']['authors']
#    book['volumeInfo']['imageLinks']['smallThumbnail'])

# books object is defined. List of dictionaries, one for each item.
    books = [{'title': None, 'authors': None, 'ISBN': None, 'description': None, 'image': None}
             for x in range(len(response['items']))]

# Loop through all books provided by response
    for i in range(len(response['items'])):
        # for i in range(10):

        # Exception handling is used because some keys will be missing from the data
        try:
            response['items'][i]['volumeInfo']['title']
        except KeyError:
            books[i]['title'] = 'Not Available'
        else:
            books[i]['title'] = response['items'][i]['volumeInfo']['title']

# Exception handling
        try:
            response['items'][i]['volumeInfo']['authors'][0]
        except KeyError:
            books[i]['authors'] = 'Not Available'
        else:
            books[i]['authors'] = response['items'][i]['volumeInfo']['authors'][0]

# Exception handling
        try:
            response['items'][i]['volumeInfo']['industryIdentifiers'][0]['identifier']
        except KeyError:
            books[i]['ISBN'] = None
        else:
            books[i]['ISBN'] = response['items'][i]['volumeInfo']['industryIdentifiers'][0]['identifier']

# Exception handling
        try:
            response['items'][i]['volumeInfo']['description']
        except KeyError:
            books[i]['description'] = 'Not Available'
        else:
            books[i]['description'] = response['items'][i]['volumeInfo']['description']

# Exception handling. Default image, if none available, is landscape from Unsplash.com
        try:
            response['items'][i]['volumeInfo']['imageLinks']['smallThumbnail']
        except KeyError:
            books[i]['image'] = 'https://images.unsplash.com/photo-1469827160215-9d29e96e72f4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'
        else:
            books[i]['image'] = response['items'][i]['volumeInfo']['imageLinks']['smallThumbnail']

    return books


def hudate(datestring):
    """Format date in readable form"""

    # Create datetime object from string held in meetings table in database
    date_time_obj = datetime.strptime(datestring, "%Y-%m-%d")

    # Convert datetime object into human readable form
    hudatestring = date_time_obj.strftime("%d %b %Y")

    return hudatestring


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
