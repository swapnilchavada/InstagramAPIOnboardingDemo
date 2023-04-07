from flask import Flask

import os
# from config import Config, ProductionConfig, DevelopmentConfig
from config_values import DevelopmentConfig, ProductionConfig

app = Flask(__name__)
c = DevelopmentConfig()
app.config.from_object(c)

from app import routes
