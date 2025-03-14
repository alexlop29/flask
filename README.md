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

### Security
HTML is the default flask response type.

Leverage HTML escaping for any user-provided values to prevent
injection attacks.