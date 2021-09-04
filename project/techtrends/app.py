import sqlite3
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
loghandler = logging.StreamHandler()
loghandler.setFormatter(
        logging.Formatter("%(levelname)s:%(name)s:%(asctime)s, %(message)s", "%m/%d/%Y, %H:%M:%S")
    )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(loghandler)

totDBConn = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global totDBConn
    totDBConn = totDBConn + 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()

    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
# app.logger.addHandler(loghandler)
# logging.getLogger('werkzeug').disabled = True
# logging.getLogger('werkzeug').addHandler(loghandler) 
if len(logging.getLogger('werkzeug').handlers) == 0:
    logging.getLogger('werkzeug').addHandler(logging.StreamHandler())

loghandler = logging.getLogger('werkzeug').handlers[0]
loghandler.setFormatter(
        logging.Formatter(
            # f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
            "%(levelname)s:%(name)s:%(message)s"
        )
    )

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:                
        logger.info("Article \"{0}\" NOT FOUND.".format(post_id))
        return render_template('404.html'), 404
    else:
        # POST TITLE is located a Index 2
        logger.info("Article \"{0}\" retrived.".format(post[2]))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.info("About Us")
    return render_template('about.html')

# Define the Health Status endpoint
@app.route('/healthz')
def healthz():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    totpost = connection.execute('SELECT COUNT(id) FROM posts').fetchall()[0][0]
    connection.close()

    response = app.response_class(
            # TODO: Hardcoded DB Connection Count and Post Count to be changed
            response=json.dumps({"status":"success","code":0,"data":{"db_connection_count": totDBConn, "post_count": totpost}}),
            status=200,
            mimetype='application/json'
    )
    return response

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            logger.info("Article \"{0}\" recorded.".format(title))

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
