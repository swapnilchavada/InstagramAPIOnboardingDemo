import os

class Config(object):
    DEBUG = False
    TESTING = False
    APP_ID = 1250771592189033
    APP_SECRET = '1cc08bed191745c4c5447600e2ae82e9'
    BASE_GRAPH_API_URL = 'https://graph.facebook.com/v16.0/'
    REDIRECT_URL = 'https%3A%2F%2F127.0.0.1:5000%2Flogin_success'

class ProductionConfig(Config):
    REDIRECT_URL = 'https%3A%2F%2Fig-business-onboarding-demo-1.herokuapp.com%2Flogin_success'

class DevelopmentConfig(Config):
    DEBUG = True
    REDIRECT_URL = 'https%3A%2F%2F127.0.0.1:5000%2Flogin_success'
