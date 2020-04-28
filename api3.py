from flask import Flask, jsonify,render_template, request, Response
import json
import hashlib
import math
import requests
from collections import defaultdict
# step 1: import the redis-py client package
import redis
import sys
import argparse
import time

app = Flask(__name__)
app.config["DEBUG"] = True

redis_host = "redis"
redis_port = 6379
redis_password = ""

r = redis.Redis(host=redis_host, port=redis_port)
mkeys = []


#if __name__ == '__main__':
    #hello_redis()


@app.route("/")
def home():
	return "Hello World"
	
	#this will display html form ready for input!
	#return render_template('index.html')
		
@app.route('/keyval', methods=['POST'])
def add_key():
	#global mkeys
	
	key = request.get_json()
	
	mkeys.append(key)
	d = json.dumps(mkeys)
	
	#r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)   

	for item in mkeys:
		# Set the fields in Redis
		ret = r.set("mykey",list( item.keys() )[0],86400)	
		ret = r.set("myvalue",list( item.values() )[0],86400)
		#r.set("my_value", list( item.values() )[0])
		#r.set("my_command", "CREATE new-key/new-value")
		
		#will return value of json object sent 
		#return ( list( item.values() )[0] )
		#results = {}
		if ret:
			msg = "CREATE new-key/new-value"
			status = 200
		else:
			msg = "Unable to CREATE new-key/new-value"
			status = 400
		
		#this causes error, connection error to redis ?? 
		data = {
			'key'  : r.get("mykey"),
			'value' : r.get("myvalue"),
			'command': msg,
			'result': ret,
			'error': ""
		}
	
		js = json.dumps(data)
		#js = jsonify(data)

		resp = Response(js, status=status, mimetype='application/json')
		
		return resp
		#return r.get("my_key")
		
		
@app.route('/keyval', methods=['PUT'])
def update_key():
	#mkeys = []
	key = request.get_json()
	
	mkeys.append(key)
	d = json.dumps(mkeys)
	
	#r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)   

	for item in mkeys:
		# Set the fields in Redis
		ret = r.set("mykey",list( item.keys() )[0],86400)	
		ret = r.set("myvalue",list( item.values() )[0],86400)
		#r.set("my_value", list( item.values() )[0])
		#r.set("my_command", "CREATE new-key/new-value")
		
		#will return value of json object sent 
		#return ( list( item.values() )[0] )
		#results = {}
		if ret:
			msg = "Updated " + r.get("mykey") + " with new value " + r.get("myvalue")
			status = 200
		else:
			msg = "Unable to Update key " + r.get("mykey")
			status = 400
		
		#this causes error, connection error to redis ?? 
		data = {
			'key'  : r.get("mykey"),
			'value' : r.get("myvalue"),
			'command': msg,
			'result': ret,
			'error': ""
		}
	
		js = json.dumps(data)
		#js = jsonify(data)

		resp = Response(js, status=status, mimetype='application/json')
		
		return resp

@app.route('/keyval/<mstring>', methods=['DELETE'])
def delete_key(mstring):
	#mkeys = []
	#mkeys.pop(mstring)
	#return 'None', 200
	okey = r.get("mykey")
	ovalue = r.get("myvalue")
	ret = r.delete("mykey",mstring)
	if ret:
		msg = "DELETE " + okey
		status = 200	
	else:
		msg = "No such key exists"
		status = 400 
		
	#this causes error, connection error to redis ?? 
	data = {
		'key'  : okey,
		'value' : ovalue,
		'command': msg,
		'result': ret,
		'error': status
	}
	
	js = json.dumps(data)
	#js = jsonify(data)

	resp = Response(js, status=status, mimetype='application/json')
		
	return resp
	
@app.route('/keyval/<mstring>', methods=['GET'])
def get_key(mstring):
	ret = r.get(mstring)
	#ovalue = r.get("myvalue")
	
	if ret:
		msg = "GET " + okey
		status = 200	
	else:
		msg = "No such key exists"
		status = 400 
		
	#this causes error, connection error to redis ?? 
	data = {
		'key'  : mstring,
		'value' : ret,
		'command': msg,
		'result': ret,
		'error': status
	}
	
	js = json.dumps(data)
	#js = jsonify(data)

	resp = Response(js, status=status, mimetype='application/json')
		
	return resp

@app.route('/clear', methods=['GET'])
def clear_data():
    r.flushall()
    return "All Keys/Value pairs Removed"

@app.route('/md5/<mstring>')
def api_str(mstring):
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	#if 'str' in request.args:
	

		 
	hstr=hashlib.md5(mstring.encode()).hexdigest()
	
	data = {
		'input'  : mstring,
		'output' : hstr
	}
	
	js = json.dumps(data)
	#js = jsonify(data)

	resp = Response(js, status=200, mimetype='application/json')
	
	return resp
	
	#return "Input: " + string + " Output: " + hstr
	#else:
		#return "Error: No id field provided. Please specify an id."

@app.route('/factorial/<int:myint>')
def api_factor(myint):
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	#if 'str' in request.args:
		n = int(myint)
		if n<0:
			return "Plese enter a positive integer!"
		else:	
			hstr=math.factorial(int(myint))
			data = {
				'input'  : myint,
				'output' : hstr
			}
	
			js = json.dumps(data)

			resp = Response(js, status=200, mimetype='application/json')
	
			return resp	
			#return "Input: " + myint + " Ouptut: " + str(hstr)
	#else:
		#return "Error: No id field provided. Please specify an id."

@app.route('/fibonacci/<int:myint>')
def api_fibonacci(myint):
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	#if 'str' in request.args:
	
		def recur_fibo(n):
			if n <= 1:
				return n

			return(recur_fibo(n-1) + recur_fibo(n-2))
			
		nterms = int(myint)
		# Python program to display the Fibonacci sequence
		# check if the number of terms is valid
		if nterms <= 0:
			return "Plese enter a positive integer!"
		else:
			#return "Fibonacci sequence: "
			a=[]
			for i in range(0, nterms+3):
				m = recur_fibo(i)
				if m > nterms:
					break    # break here   
				a.append(m)
			
			data = {
				'input'  : myint,
				'output' : a
			}
	
			js = json.dumps(data)

			resp = Response(js, status=200, mimetype='application/json')
	
			return resp				
			#return "Input: " + myint + "  Ouptut: " + str(a)
	#else:
		#return "Error: No id field provided. Please specify an id."		

@app.route('/is-prime/<int:myint>')
def api_prime(myint):
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	#if 'str' in request.args:
		n = int(myint)
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
		
			hstr=int(myint)
			#if(isPrime(hstr)) : 
			data = {
				'input'  : myint,
				'output' : isPrime(hstr)
			}
	
			js = json.dumps(data)

			resp = Response(js, status=200, mimetype='application/json')
	
			return resp			
				#return "Input: " + myint + " Output: TRUE"
			#else :  
				#return "Input: " + myint + " Output: FALSE"
			
	#else:
		#return "Error: No id field provided. Please specify an id."
		
@app.route('/slack-alert/<string>')
def api_slack(string):
	# Check if an str was provided as part of the URL.
	# If str is provided, assign it to a variable.
	# If no ID is provided, display an error in the browser.
	#if 'str' in request.args:
		hstr = string
		# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
		webhook_url = 'https://hooks.slack.com/services/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'
		#https://tcmg412.slack.com/files/U257RQGDB/F0114JWNZQE/kanban_-_david_anderson_-_excerpts.pdf
		slack_data = {'text': hstr}
			
		response = requests.post(
			webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
		)
		if response.status_code != 200:
			mbool = False
			raise ValueError(
			'Request to slack returned an error %s, the response is:\n%s'
			#data.append({'output':response.status_code})
				% (response.status_code, response.text)
			)
		if response.status_code == 200:
			#data.append({'output':response.status_code})
			#return "Your message was sucessfully posted!"
			mbool = True
			
		data = {
			'input'  : hstr,
			'output' : mbool
		}
		
		js = json.dumps(data)
		#js = jsonify(data)

		resp = Response(js, status=200, mimetype='application/json')
	
		return resp
	#else:
		#return "Error: No id field provided. Please specify an id."
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  
