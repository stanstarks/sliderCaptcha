# sliderCaptcha-django

A python-django toy project hybriding [visualCaptcha](https://github.com/emotionLoop/visualCaptcha-python) and [QapTcha]()


## Installation 

You need Python installed with pip.
```
pip install -r requirements.txt
```

In current settings, `memcached` is used for django in memory cache. The default port is localhost:11211. However, built-in default local memory also works. You can change the `CACHES` settings in `settings.py`.


## Run server

First make sure memcached is running on 11211. Or start it with
```
$ memcached
```

To start the server on port, for example, 8282, run the following command:
```
$ python manage.py runserver 0.0.0.0:8282
```

## Run tests

If you want to run the unit tests, use the following command:
```
python manage.py test
```


## API

I adopted the visualCaptcha utilities and left the APIs unchanged. (But you have to include the js/css code if you want to use.)

Following are added:

### GET `/startslider`

This route will be the first route called by the front-end, which will generate and store session data.

### GET `/slider(/:foreground)`

This route will be called for the slider image

Parameters:

- `foreground` is optional means fetching slider image.

### POST `/scroll` 

This route is where the sliderCaptcha validation takes place.


## License

MIT. Check the [LICENSE](LICENSE) file.
