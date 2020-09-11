#!/usr/bin/env python3

from flask import Flask, request, render_template
import numpy as np
import json
import re
from pymongo import MongoClient
from bson.code import Code

client = MongoClient("localhost", 27017)
db = client.moviemeta

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html", frq=wordcloud())


@app.route('/fetch')
def submit():
	term = request.args['term']
	resp = []
	if term:
		res = db.movies.find({"title": re.compile(term, re.IGNORECASE)}, {"_id": 0, "title": 1}, sort=[("title", 1)], limit=12)
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
	genreCount = db.movies.map_reduce(map, reduce, "genreCount")
	return genreCount


mapred_count = 0
update_int = 40


def wordcloud():
	global mapred_count
	if not mapred_count % update_int:
		genreCount = get_genre_count()
	else:
		genreCount = db.genreCount
	mapred_count = (mapred_count + 1) % update_int
	frq = []
	mxvl = 0
	for doc in genreCount.find():
		dct = {"text": doc["_id"], "size": doc["value"]}
		if doc["value"] > mxvl:
			mxvl = doc["value"]
		frq.append(dct)
	for dct in frq:
		dct["size"] = 15 + int(130 * dct["size"] / mxvl)
	return frq


if __name__ == '__main__':
	app.run(debug=False)
#	app.run(host='0.0.0.0', port=31796, debug=False)
