from flask import Flask, escape, request
import hashlib
import json

app = Flask("api")
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1> This is a Test </h1> <p>If you seen then I think this worked. </p>"

@app.route('/md5/<anystring>')
def md5_str(anystring):
    val = request.args.get("str")
    m = hashlib.md5(val.encode())

    output = {
        "input": val,
        "output": m.hexdigest()
    }

    return json.dumps(output)


app.run()