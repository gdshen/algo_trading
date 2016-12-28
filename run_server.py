from app import app
from auth import auth_flask_login

app.register_blueprint(auth_flask_login)

if __name__ == '__main__':
    if app.config['SSL_OR_NOT']:
        context = ('trade_gdshen_me.crt', 'trade_gdshen_me.key')
        app.run(host='0.0.0.0', port=443, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=80)
        #app.run(port=8080)
