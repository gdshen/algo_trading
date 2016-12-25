# setting debug mode
DEBUG = True

# secret_key that need to make CSRF protection
SECRET_KEY = 'this_is_a_secret_key'

# add mongoengine to flask_debugtoolbar view
DEBUG_TB_PANELS = ['flask_mongoengine.panels.MongoDebugPanel']

# setting flask_debugtoolbar whether intercept redirect
DEBUG_TB_INTERCEPT_REDIRECTS = False

# setting https mode or not
# SSL_OR_NOT = True
SSL_OR_NOT = False

# mongodb database access configuration
MONGODB_SETTINGS = {
    'db': 'trade',
    'host': 'lab.gdshen.me',
    'port': 27017
}

MONGODB_URL = 'mongodb://lab.gdshen.me:27017'

MARKET_MORNING_OPEN = "09:30"
MARKET_MORNING_CLOSE = "11:30"
MARKET_AFTERNOON_OPEN = "13:00"
MARKET_AFTERNOON_CLOSE = "15:00"
