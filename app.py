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


@app.errorhandler(404)
def not_found(error):
    """
    If API aborts due to invalid input, return the below response.
    :param error: The error that caused the abort
    :return: JSON Object
    """
    return make_response(jsonify({'message': 'Not found, Invalid Parameters or URL'}), 404)


@app.errorhandler(403)
def not_found(error):
    """
    If API aborts due to invalid input, return the below response.
    :param error: The error that caused the abort
    :return: JSON Object
    """
    return make_response(jsonify({'message': 'Forbidden. Private Subreddit'}), 404)


def check_valid(args):
    """
    Checks to see if the given arguments are valid
    :param args: The arguments to check
    :return: Whether or not they are valid
    """
    for arg in args:
        if not valid_args[arg]:
            return False
    return True


# ------------------------------------------------------------------------------------------------------
@app.route("/")
def inital():
    """
    Initial Template Render: Renders the index.html page.
    :return: Response
    """
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('index.html'), 200, headers)


@app.route('/view/<string:type>', methods=['POST'])
def static_page(type):
    """
    Renders the sub_view html page given a type of listing
    :param type:
    :return: Response
    """
    result = dict(ImmutableMultiDict(request.form))
    subreddit = result["subreddit_chose"][0].replace(" ", "")
    print("Listing Type:", type)
    print("Subreddit:", subreddit)
    # reroute_url = request.url_root + "api/v1.0/r/" + subreddit + "/" + type + "/" + "limit=20"
    # data = requests.post(reroute_url)
    data = connect.get_type_post(subreddit, type, 40) # Used for Local Testing
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('sub_view.html', subreddit=subreddit, data=data, list_type=type), 200, headers)


@app.route('/view/r/<string:subreddit>/<string:type>', methods=['POST', 'GET'])
def static_page_cont(subreddit, type):
    if request.method == 'POST':
        result = dict(ImmutableMultiDict(request.form))
        new_subreddit = result["subreddit_chose"][0].replace(" ", "")
        print("Listing Type:", type)
        print("Subreddit:", new_subreddit)
        # reroute_url = request.url_root + "api/v1.0/r/" + new_subreddit + "/" + type + "/" + "limit=20"
        # data = requests.post(reroute_url)
        data = connect.get_type_post(new_subreddit, type, 40) # Used for Local Testing
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sub_view.html', subreddit=new_subreddit, data=data, list_type=type), 200,
                             headers)
    else:
        # reroute_url = request.url_root + "api/v1.0/r/" + subreddit + "/" + type + "/" + "limit=20"
        # data = requests.post(reroute_url)
        data = connect.get_type_post(subreddit, type, 40) # Used for Local Testing
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sub_view.html', subreddit=subreddit, data=data, list_type=type), 200,
                             headers)


if __name__ == '__main__':
    app.run(debug=True)
