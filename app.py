import os
import json
import urllib
import pickle as pk
import numpy as np

from os.path import join, dirname, realpath
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash, Response, jsonify
from werkzeug.utils import secure_filename

import score

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/') # where uploaded files are stored
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF']) # models support png and gif as well

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # max upload - 10MB
app.secret_key = 'secret'

def allowed_file(filename):
    	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
	return render_template('index.html', result=None)

@app.route('/assessment', methods=['GET', 'POST'])
def upload_and_classify():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('assess'))
		
		file = request.files['file']

		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(url_for('assess'))

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename) # used to secure a filename before storing it directly on the filesystem
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			images, distances = score.closest(filepath)

			return jsonify(images=images,distances=distances)
	
	flash('Invalid file format - please try your upload again.')
	return redirect(url_for('assess'))


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False) # remember to set back to False	