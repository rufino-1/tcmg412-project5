from flask import Flask, render_template, request
import json, pandas as pd
import hashlib
import math

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def home():
        return render_template('index.html')

@app.route('/api/astrosplayers/all', methods=['GET'])
def GetData():
    df = pd.read_csv("DemoData.csv")
    temp = df.to_dict('records')
    columnNames = df.columns.values
    return render_template('record.html', records=temp, colnames=columnNames)

@app.route('/api/md5', methods=['GET'])
def api_str():
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	if 'str' in request.args:
		
		hstr=hashlib.sha224(request.args['str'].encode()).hexdigest()
		return "This is the hashed Value of " + request.args['str'] + ": " + hstr
	else:
		return "Error: No id field provided. Please specify an id."

@app.route('/api/factorial', methods=['GET'])
def api_factor():
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	if 'str' in request.args:
		n = int(request.args['str'])
		if n<0:
			return "Plese enter a positive integer!"
		else:	
			hstr=math.factorial(int(request.args['str']))
			return "This is the factorial value of " + request.args['str'] + ": " + str(hstr)
	else:
		return "Error: No id field provided. Please specify an id."

@app.route('/api/fibonacci', methods=['GET'])
def api_fibonacci():
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	if 'str' in request.args:
	
		def recur_fibo(n):
			if n <= 1:
				return n
			else:
				return(recur_fibo(n-1) + recur_fibo(n-2))
				
		nterms = int(request.args['str'])
		# Python program to display the Fibonacci sequence
		# check if the number of terms is valid
		if nterms <= 0:
			return "Plese enter a positive integer!"
		else:
			#return "Fibonacci sequence: "
			a=[]
			for i in range(nterms):
				a.append(recur_fibo(i))
				
			return "The fibonacci sequence for " + request.args['str'] + " is: " + str(a)
	else:
		return "Error: No id field provided. Please specify an id."		

@app.route('/api/is-prime', methods=['GET'])
def api_prime():
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	if 'str' in request.args:
		n = int(request.args['str'])
		if n<0:
			return "Plese enter a positive integer!"
		else:	
		
			def isPrime(n) : 
  				# Corner cases 
				if (n <= 1) : 
					return False
				if (n <= 3) : 
					return True
					
  				# This is checked so that we can skip  
				# middle five numbers in below loop 
				if (n % 2 == 0 or n % 3 == 0) : 
					return False
  
				i = 5
				while(i * i <= n) : 
					if (n % i == 0 or n % (i + 2) == 0) : 
						return False
					i = i + 6
					
				return True
		
			hstr=int(request.args['str'])
			if(isPrime(hstr)) : 
				return "The given value of " + request.args['str'] + " IS a Prime Number!"
			else :  
				return "The given value of " + request.args['str'] + " IS NOT a Prime Number!"
			
	else:
		return "Error: No id field provided. Please specify an id."
		
@app.route('/api/slack-alert', methods=['POST'])
def api_slack():
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	if 'str' in request.args:
		hstr = request.args['str']
		# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
		webhook_url = 'https://tcmg412.slack.com/archives/C2581UKGA'
		#https://tcmg412.slack.com/files/U257RQGDB/F0114JWNZQE/kanban_-_david_anderson_-_excerpts.pdf
		slack_data = {'text': hstr.encode() + " @TCMG412GRP3 :spaghetti:"}

		response = requests.post(
			webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
		)
		if response.status_code != 200:
			raise ValueError(
			'Request to slack returned an error %s, the response is:\n%s'
				% (response.status_code, response.text)
			)
		if response.status_code == 200:
			return "Your message was sucessfully posted!"
	else:
		return "Error: No id field provided. Please specify an id."
app.run()  