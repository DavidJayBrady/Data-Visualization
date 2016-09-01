'''
To run this program, navigate to the directory with server.py, and type the following commands:
export FLASK_APP=server.py
flask run
'''

# This file is responsible for 2 things:
# 1. Running the server. The default port is 5000.
# 2. Calling the right code at the right time

import flask
from graph import update_png

# static_folder is looked for by flask for Assets. In this case, we need it for the png
app = flask.Flask(__name__, static_folder="/Users/Owner/Desktop/Programming/Data Visualization")

# "/" is the homepage. This function is called when a browser navigates to 10.10.10.10:5000/
# Note: Enjoy the fake IP address

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('interface.html')

# This function is called when the submit button from the html page gets clicked.
# This happens because the form tag has the following: action="/my-link" method="POST"
@app.route("/my-link/", methods=["POST"])
def my_link():
    if flask.request.method == "POST":

        # Grab the info from the radio buttons/text field.
        type_of_graph = flask.request.form.get("graph", None)
        constraints = flask.request.form.get("constraints", None)

        # Update the png
        update_png(type_of_graph, constraints)

        # Go back to the home page. Refresh to reload the new png, if it was made (it may not have
        # refreshed if no radio was selected)
        return flask.redirect("/")