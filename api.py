import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
astrosplayers = [
	{'id': 0,
     'name': 'Craig Biggio',
     'position': 'second base',
     'allstar appearances': 'seven',
     'championships': '0'},
    {'id': 1,
     'name': 'Jose Altuve',
     'position': 'second base',
     'allstar appearances': 'six',
     'championships': '1'},
    {'id': 2,
     'name': 'Nolan Ryan',
     'position': 'pitcher',
     'allstar appearances': 'eight',
     'championships': '1'}
]

@app.route('/', methods=['GET'])
def home():
	return '''<h1>Group Project Four</h1>
<p>This site is a prototype API for Group Project Four Made by Group Three.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/astrosplayers/all', methods=['GET'])
def api_all():
	return jsonify(astrosplayers)

app.run()


@app.route('/api/v1/resources/astrosplayers', methods=['GET'])
def api_id():
	# Check if an ID was provided as part of the URL.
	# If ID is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	if 'id' in request.args:
		id = int(request.args['id'])
	else:
		return "Error: No id field provided. Please specify an id."
	
	# Create an empty list for our results
	results = []
	
	# Loop through the data and match results that fit the requested ID.
	# IDs are unique, but other fields might return many results
	for astrosplayer in astrosplayers:
		if astrosplayer['id'] == id:
			results.append(astrosplayer)
			
	# Use the jsonify function from Flask to convert our list of
	# Python dictionaries to the JSON format.
	return jsonify(results)
	
app.run()