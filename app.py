#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, render_template, request
import requests
from reddit_connect import Reddit
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
connect = Reddit()

"""
The Valid Arguments for a List Type
"""
valid_args = {
    "top": True,
    "controversial": True,
    "rising": True,
    "new": True,
}


# ------------------------------------------------------------------------------------------------------
@app.route('/api/v1.0')
def welcome():
    """
    With no path specified, returns the following welcome message.
    :return: a JSON Welcome
    """
    welcome_msg = {
        "message": "Welcome to the RTop API",
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
    if not check_valid([list_type]) or int(limit) > 100 or int(limit) < 0:
        abort(401)
    """
    :param subreddit: The subreddit to retrieve the top posts from
    :param list_type: The type of posts to retrieve
    :param limit: the number of posts to get
    :return: JSON Object
    """
    response = connect.get_type_post(subreddit, list_type, limit)
    if "posts" in response and not response["posts"]:
        abort(401)
    return make_response(jsonify(response), 200)


@app.errorhandler(401)
def not_found_404(error):
    """
    If API aborts due to invalid input, return the below response.
    :param error: The error that caused the abort
    :return: JSON Object
    """
    return make_response(jsonify({'message': 'Not found, Invalid Parameters or URL'}), 401)


@app.errorhandler(403)
def not_found_403(error):
    """
    If API aborts due to a private subreddit or empty one return the below response.
    :param error: The error that caused the abort
    :return: JSON Object
    """
    return make_response(jsonify({'message': 'Forbidden. Private Subreddit'}), 403)


@app.errorhandler(500)
def not_found_500(error):
    """
    If there is some internal error
    :return: JSON Object
    """
    return make_response(jsonify({'message': 'Something went really wrong: Internal Server Error'}), 500)


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
    :param type: The listing type to display
    :return: Response
    """
    result = dict(ImmutableMultiDict(request.form))
    new_subreddit = result["subreddit_chose"][0].replace(" ", "")
    print("Listing Type:", type)
    print("Subreddit:", new_subreddit)
    # reroute_url = "https://rtop.herokuapp.com/" + "api/v1.0/r/" + new_subreddit + "/" + type + "/" + "limit=40" # UNCOMMENT FOR LOCAL TESTING
    reroute_url = request.url_root + "api/v1.0/r/" + new_subreddit + "/" + type + "/" + "limit=40" # COMMENT OUT FOR LOCAL TESTING
    data = requests.post(reroute_url).json()
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('sub_view.html', subreddit=new_subreddit, data=data, list_type=type), 200,
                         headers)


@app.route('/view/r/<string:subreddit>/<string:type>', methods=['POST', 'GET'])
def static_page_cont(subreddit, type):
    """
    Renders the static page given a subreddit and a type
    :param subreddit: The subreddit whose posts you want to render
    :param type: The type of listing (top, new, controversial, rising)
    :return: Response
    """
    if request.method == 'POST':
        result = dict(ImmutableMultiDict(request.form))
        new_subreddit = result["subreddit_chose"][0].replace(" ", "")
        print("Listing Type:", type)
        print("Subreddit:", new_subreddit)
        # reroute_url = "https://rtop.herokuapp.com/" + "api/v1.0/r/" + new_subreddit + "/" + type + "/" + "limit=40" # UNCOMMENT FOR LOCAL TESTING
        reroute_url = request.url_root + "api/v1.0/r/" + new_subreddit + "/" + type + "/" + "limit=40"  #COMMENT OUT FOR LOCAL TESTING
        data = requests.post(reroute_url).json()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sub_view.html', subreddit=new_subreddit, data=data, list_type=type), 200,
                             headers)
    else:
        # reroute_url = "https://rtop.herokuapp.com/" + "api/v1.0/r/" + subreddit + "/" + type + "/" + "limit=40" # UNCOMMENT FOR LOCAL TESTING
        reroute_url = request.url_root + "api/v1.0/r/" + subreddit + "/" + type + "/" + "limit=40" # COMMENT OUT FOR LOCAL TESTING
        data = requests.post(reroute_url).json()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sub_view.html', subreddit=subreddit, data=data, list_type=type), 200,
                             headers)


if __name__ == '__main__':
    app.run(debug=True)
