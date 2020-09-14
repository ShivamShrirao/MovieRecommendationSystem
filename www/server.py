#!/usr/bin/env python3

from flask import Flask, request, render_template, url_for
from sentence_transformers import util
import torch
import numpy as np
import json
import re
from pymongo import MongoClient
from bson.code import Code

client = MongoClient("localhost", 27017)
db = client.moviemeta

corpus_embeddings = torch.load('datasets/corpus_embeddings.pt')

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html", frq=wordcloud())


@app.route('/bar_graph')
def bar_graph():
	return render_template("bar_graph.html")


@app.route('/fetch')
def submit():
	term = request.args['term']
	resp = []
	if term:
		res = db.movies.find({"title": re.compile(term, re.IGNORECASE)}, {"_id": 0, "title": 1, "id": 1, "poster_path": 1},
				sort=[("vote_weight", -1), ("title", 1)],
				limit=12)
		for nm in res:
			resp.append({
					"value": nm["title"],
					"label": "<img src='https://image.tmdb.org/t/p/w92" + str(nm["poster_path"]) + "' height='70' />" + str(nm["title"]),
					"url": url_for('about', id=nm["id"])
					})
	return json.dumps(resp)


@app.route('/search')
def search():
	res = []
	term = None
	try:
		term = request.args['q']
		if term:
			res = db.movies.find({"title": re.compile(term, re.IGNORECASE)}, {"_id": 0}, sort=[("vote_weight", -1), ("title", 1)], limit=30)
	except KeyError:
		pass
	return render_template("search.html", qtype="Search", res=res, query=term)


@app.route('/filter/<genre>')
def filter(genre):
	res = []
	try:
		res = db.movies.find({"genres": genre}, {"_id": 0}, sort=[("vote_weight", -1)], limit=30)
	except KeyError:
		pass
	return render_template("search.html", qtype="Filter", res=res, query=genre)


def get_recommendations(idx, top_k=31):
	cur_embedding = corpus_embeddings[idx]
	cos_scores = util.pytorch_cos_sim(cur_embedding, corpus_embeddings)[0]
	cos_scores = cos_scores.cpu()
	top_results = np.argpartition(-cos_scores, range(top_k))
	return top_results[1:top_k], cos_scores


@app.route('/about/<id>')
def about(id):
	ret = db.movies.find_one({"id": int(id)}, {"_id": 0})
	similar = []
	if ret is None:
		ret = {"title": "Not Found!"}
	else:
		top_results, cos_scores = get_recommendations(ret["idx"])
		for i in top_results:
			similar.append(db.movies.find_one({"idx": i.item()}, {"_id": 0}))
			similar[-1]["cos_score"] = cos_scores[i].item()
		similar[:15] = sorted(similar[:15], key=lambda e: e["vote_weight"]*e["cos_score"], reverse=True)
	return render_template("about.html", main_movie=ret, similar=similar)


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
