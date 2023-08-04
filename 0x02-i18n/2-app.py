#!/usr/bin/env python3
''' Get locale from request'''
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
    ''' a function that gets local'''
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    ''' a simple flask route'''
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run()
