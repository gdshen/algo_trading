DEBUG = True
SECRET_KEY = 'this_is_a_secret_key'
DEBUG_TB_PANELS = ['flask_mongoengine.panels.MongoDebugPanel']
DEBUG_TB_INTERCEPT_REDIRECTS = False

MONGODB_SETTINGS = {
    'db': 'trade',
    'host': '127.0.0.1',
    'port': 27017
}
