#!/usr/bin/python3
# --------------------------
# run a display front end
# --------------------------

import flask 
import os 
import pandas

import werkzeug

DEBUG    = os.environ.get('DEBUG', True)
HOST     = os.environ.get('HOST', '0.0.0.0')
PORT     = int(os.environ.get('PORT', 8080))
TMPL_DIR = os.path.abspath('html_templates')
UPLOAD_FOLDER = '/tmp'

app = flask.Flask(__name__, template_folder = TMPL_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():

   # show a very minimal interface for uplaoding a file
   if flask.request.method == 'GET':
      return flask.render_template('upload.html')

   # now do the intersting stuff
   if flask.request.method == 'POST':

      # get the file content and save it under /tmp
      f = flask.request.files['file']
      filename = os.path.join (app.config['UPLOAD_FOLDER'], werkzeug.utils.secure_filename(f.filename))
      f.save (filename)

      # use pandas to read the newly created file and convert it into a dictionnary 
      # taking the first row as headers
      content = pandas.read_csv(filename).to_dict(orient='records')
      # dump the content as a table
      return flask.render_template('result.html', data = content)

      
if __name__ == '__main__':
   app.run(debug = DEBUG, host = HOST, port = PORT)

