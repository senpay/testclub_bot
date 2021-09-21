import os
from flask import Flask

import logging
logging.basicConfig(level=logging.INFO)


app=Flask(__name__,instance_relative_config=True)
app.secret_key = 'dev'

@app.route('/hello')
def hello():
    return "Hello, World!"