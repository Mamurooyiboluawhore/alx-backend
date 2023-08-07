#!/usr/bin/env python3
''' Basic Babel setup'''
from flask import Flask, g, render_template, request
from flask_babel import Babel
from typing import Dict


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    ''' a config class'''
    LANGUAGES = ["en", "fr"]

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    ''' a function that gets local'''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id):
    '''a function that fetches users from mock db'''
    return users.get(user_id)


@app.before_request
def before_request():
    ''' before request function'''
    user_id = request.args.get('login_as')
    if user_id:
        user_id = int(user_id)
        g.user = get_user(user_id)
    else:
        g.user = None


@app.route('/')
def index():
    ''' a simple flask route'''
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")
