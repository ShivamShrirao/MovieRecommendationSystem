#!/usr/bin/env python3

from flask import Flask, request, render_template
import numpy as np
import json
import re
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
	resp = []
	if term:
		res = db.movies.find({"title": re.compile(term, re.IGNORECASE)}, {"_id": 0, "title": 1}, limit=15)
		for nm in res:
			resp.append(nm["title"])
	return json.dumps(resp)


if __name__ == '__main__':
	app.run(debug=True)
