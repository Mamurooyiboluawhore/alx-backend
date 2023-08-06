#!/usr/bin/env python3
''' Basic Babel setup'''
from flask import Flask, render_template, request
from flask_babel import Babel


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


app.config.from_object(Config)


@app.route('/')
def index():
    ''' a simple flask route'''
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")
