#!/usr/bin/env python3

from flask import Flask, request, render_template
import numpy as np
import json
import re
from pymongo import MongoClient
from bson.code import Code

client = MongoClient("localhost", 27017)
db = client.IMDB

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html", frq=wordcloud())


@app.route('/fetch')
def submit():
	term = request.args['term']
	resp = []
	if term:
		res = db.movies.find({"title": re.compile(term, re.IGNORECASE)}, {"_id": 0, "title": 1}, limit=12)
		for nm in res:
			resp.append(nm["title"])
	return json.dumps(resp)


@app.route('/about')
def about():
	resp = {"title": "Title"}
	try:
		term = request.args['q']
		if term:
			resp = db.movies.find_one({"title": term}, {"_id": 0})
	except KeyError:
		pass
	return render_template("about.html", resp=resp)


def get_genre_count():
	map = Code("function() {"
			   "	this.genres.forEach(function(gnr){"
			   "		emit(gnr, 1);"
			   "	})"
			   "}")

	reduce = Code("function(key, values) {"
				  "		return Array.sum(values)"
				  "}")
	results = db.movies.map_reduce(map, reduce, "results")
	return results


def wordcloud():
	results = get_genre_count()
	frq = []
	mxvl = 0
	for doc in results.find():
		dct = {}
		dct["text"] = doc["_id"]
		dct["size"] = doc["value"]
		if doc["value"] > mxvl:
			mxvl = doc["value"]
		frq.append(dct)
	for dct in frq:
		dct["size"] = 20 + int(120*dct["size"]/mxvl)
	return frq


if __name__ == '__main__':
	app.run(debug=True)
