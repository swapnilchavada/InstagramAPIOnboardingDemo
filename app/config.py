import os

class Config(object):
    DEBUG = False
    TESTING = False
    APP_ID = 276017384751834
    APP_SECRET = 'a382b17e1f1ff4ab537ecb909bdba9c9'
    BASE_GRAPH_API_URL = 'https://graph.facebook.com/v16.0/'
    REDIRECT_URL = 'https%3A%2F%2F127.0.0.1:5000%2Flogin_success'

class ProductionConfig(Config):
    REDIRECT_URL = 'https%3A%2F%2Fwww.yzs3rdpartytestapp.com%2Ftest'

class DevelopmentConfig(Config):
    DEBUG = True
    REDIRECT_URL = 'https%3A%2F%2F127.0.0.1:5000%2Flogin_success'
