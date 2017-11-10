# RTop: https://rtop.herokuapp.com/

RTop is a basic subreddit restyler that utilizes data pulled from the RTop API to visualize subreddit content.

### How It Works

Using the Reddit API, I developed a 'wrapper' API using Python Flask that pulls information from the Reddit API, simplifies it to only include relevant information, and then returns the neccesary response. Using the data returned from the RTop API, I rendered HTML templates through Python Flask's template functionality and jinja2 to create a basic website to visualize the data returned from the API. Finally, I utilized the Javascript and CSS provided by Materialize to improve the design.

### Built With

[Werkzeug](http://werkzeug.pocoo.org/): A WSGI utility library for Python.

[Flask](http://flask.pocoo.org/): A microframework for Python based on Werkzeug, Jinja 2.
```
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
 ```
 
[Materialize](http://materializecss.com/): Reresponsive front-end framework based on Material Design

[Requests](http://docs.python-requests.org/en/master/): Python HTTP library
```
 response = requests.get(self.build_url(args, limit), data=payload, headers=headers)
```
[Jinja2](http://jinja.pocoo.org/docs/2.10/): Jinja2 is a modern and designer-friendly templating language for Python
```
<ul class="tabs tabs-transparent">
                {% if list_type == 'top' %}
                    <li class="tab"><a target="_self" style="background:  #4588F1" class="active"
                                       href={{ "/view/r/" + subreddit + "/top" }}>Top</a></li>
                {% else %}
                    <li class="tab"><a target="_self" href={{ "/view/r/" + subreddit + "/top" }}>Top</a></li>
                {% endif %}
</ul>
```
[Gunicorn](http://gunicorn.org/): A Python WSGI HTTP Server for UNIX

```
web: gunicorn --pythonpath src_api app:app --log-file=-
```

### Using the API (With Requests)

Subreddit Name: All names are valid as long as they exist. If they don't exist you'll receive a Private/Empty subreddit message.
Valid Listing Types: top, rising, new, controversial
Limit: Value must be less than 100 and greater than 0. However, by default the Reddit API will return a minimum of 20 posts (If there exists that many on the subreddit).

GET
```
url = 'https://rtop.herokuapp.com/' + "api/v1.0/r/" + subreddit_name + "/" + listing_type + "/" + "limit=20"
data = requests.get(url)
```
POST
```
url = 'https://rtop.herokuapp.com/' + "api/v1.0/r/" + subreddit_name + "/" + listing_type + "/" + "limit=20"
data = requests.post(url)
```

### Deployment

Deployed using [Heroku](www.heroku.com)

### How to Build Locally

In addition to installing the dependencies above, you'll need to uncomment 3 lines of code, and comment out another three lines. In the app.py file, you'll find the lines to comment/uncomment by looking for a comment next to them like such:
```
# COMMENT OUT FOR LOCAL TESTING
# UNCOMMENT FOR LOCAL TESTING
```
The reason this is neccesarry is because the program uses the root url to determine the endpoint for get/post requests. When running locally the url is your IP address and therefore won't actually retrieve any data.

## Authors

* **Chris Risley** [CrizR](https://github.com/CrizR)
