#!/usr/bin/env python3

from flask import Flask, request, render_template
import numpy as np
import json
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.IMDB

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/fetch')
def submit():
	term = request.args['term']
	jj = [term]
	return json.dumps(jj)


if __name__ == '__main__':
	app.run(debug=True)
