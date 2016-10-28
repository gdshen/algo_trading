from app import app

if __name__ == '__main__':
    context = ('trade_gdshen_me.crt', 'trade_gdshen_me.key')
    app.run(port=443, ssl_context=context)