# RTop: https://rtop.herokuapp.com/

RTop is a basic subreddit restyler that utilizes data pulled from the RTop API to visualize subreddit content.

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

## Deployment

Deployed using [Heroku](www.heroku.com)

## Authors

* **Chris Risley** [CrizR](https://github.com/CrizR)
