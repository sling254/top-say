from flask import render_template, url_for
from . import main

@main.route('/')
def index():

    return 'Hello world'