#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, render_template, request
import requests
import json
from reddit_connect import Reddit
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
connect = Reddit()

valid_args = {
    "top": True,
    "controversial": True,
    "sort": True,
    "random": True,
    "rising": True,
    "new": True,
    "hot": True,
}


# ------------------------------------------------------------------------------------------------------
@app.route('/api/v1.0')
def welcome():
    """
    With no path specified, returns the following welcome message.
    :return: a JSON Welcome
    """
    welcome_msg = {
        "message": "Welcome to Chris Risley's RESTful Reddit API",
        "build": "Python Flask"
    }
    return make_response(jsonify(welcome_msg), 200)


@app.route('/api/v1.0/r/<string:subreddit>/<string:list_type>/limit=<int:limit>', methods=['GET', 'POST'])
def get_type_posts(subreddit, list_type, limit):
    """
    Retrieves a n number of posts (where n = limit) posts from the given subreddit
    listed in an order determined by the list_type
    :param subreddit: The subreddit to retrieve the posts form
    :param list_type: The type of listing (top, rising, new, hot ... etc.)
    :param limit: The max amount of posts to show (could be less, depends on the subreddit)
    :return: JSON Object
    """
    if not check_valid([list_type]) or int(limit) > 100 or int(limit) < 20:
        abort(404)
    """
    :param subreddit: The subreddit to retrieve the top posts from
    :param list_type: The type of posts to retrieve
    :param limit: the number of posts to get
    :return: JSON Object
    """
    response = connect.get_type_post(subreddit, list_type, limit)
    if "posts" in response and not response["posts"]:
        abort(404)
    return make_response(jsonify(response), 200)


# # TODO: Fix for templates
# @app.route('/api/v1.0', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     """
#     Catches invalid URLs
#     :param path:
#     :return: Nothing (Aborts)
#     """
#     abort(404)


@app.errorhandler(404)
def not_found(error):
    """
    If API aborts due to invalid input, return the below response.
    :param error: The error that caused the abort
    :return: JSON Object
    """
    return make_response(jsonify({'error': 'Not found, Invalid Parameters or URL'}), 404)


def check_valid(args):
    for arg in args:
        if not valid_args[arg]:
            return False
    return True


# ------------------------------------------------------------------------------------------------------
@app.route("/")
def inital():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('choose.html'), 200, headers)


@app.route('/r/<string:subreddit>/<string:list_type>/limit=<int:limit>', methods=['POST'])
def custom_static_page(subreddit, list_type, limit):
    data = json.loads(requests.post(request.url_root + "api/v1.0/" + subreddit + "/"
                                    + str(list_type) + "/" + str(limit)))
    headers = {'Content-Type': 'text/html'}
    print("test")
    return make_response(render_template('index.html', data=data), 200, headers)


@app.route('/view', methods=['POST', 'GET'])
def static_page():
    if request.method == 'POST':
        result = dict(ImmutableMultiDict(request.form))
        subreddit = result["subreddit_chose"][0]
        print(result["subreddit_chose"][0])
        reroute_url = request.url_root + "api/v1.0/r/" + subreddit + "/top/limit=20"
        print(reroute_url)
        data = connect.get_type_post(subreddit, "top", 20)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', data=data), 200, headers)


if __name__ == '__main__':
    app.run(debug=True)
