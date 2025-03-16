### Getting Started
```
pipenv install --python 3.13
pipenv shell
```

### Running
```
flask run
```

### Development 
Enable debug mode to automatically reload the server with changes.
```
flask run --debug
```

Tips
- Use the route() decorator to bind a function to a URL.
- You can add variable sections to a URL by marking sections with <variable_name>. 
- The `url_for()` function is very useful for dynamically building a URL for a specific function.
- Flask configures the Jinja2 template engine for you automatically.

### Security
- HTML is the default flask response type. Leverage HTML escaping for any user-provided values to prevent injection attacks.

### Resources
- [Flask - Docs](https://flask.palletsprojects.com/en/stable/)
- [Jinga - Docs](https://palletsprojects.com/projects/jinja/)
- [TutorialsPoint - Flask - URL Building](https://www.tutorialspoint.com/flask/flask_url_building.htm)
