#!/usr/bin/env python3
''' Basic Babel setup'''
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    ''' a config class'''
    LANGUAGES = ["en", "fr"]

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

@babel.localeselector
def get_locale():
    ''' a function that gets local'''
    return request.accept_languages.best_match(app.config['LANGUAGES'])


app.config.from_object(Config)


@app.route('/')
def index():
    ''' a simple flask route'''
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run()
