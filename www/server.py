#!/usr/bin/env python3

from flask import Flask, request, render_template
import numpy as np
import json

app = Flask(__name__)


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
	img = request.form['input']

	jj = {}
	return json.dumps(jj)


if __name__ == '__main__':
	app.run(debug=True)
