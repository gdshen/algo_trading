from app import app

if __name__ == '__main__':
    if app.config['SSL_OR_NOT']:
        context = ('trade_gdshen_me.crt', 'trade_gdshen_me.key')
        app.run(port=443, ssl_context=context)
    else:
        app.run(port=80)
