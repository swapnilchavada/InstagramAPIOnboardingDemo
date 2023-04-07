from flask import Flask

import os
# from config import Config, ProductionConfig, DevelopmentConfig
from config import DevelopmentConfig

app = Flask(__name__)
# app.config['PAGE_ACCESS_TOKEN'] = os.environ.get('PAGE_ACCESS_TOKEN')
# c = ProductionConfig()
# app.config.from_object(c)

from app import routes
