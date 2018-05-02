from flask import Flask

import os

app = Flask(__name__)
app.config['PAGE_ACCESS_TOKEN'] = os.environ.get('PAGE_ACCESS_TOKEN')

from app import routes
