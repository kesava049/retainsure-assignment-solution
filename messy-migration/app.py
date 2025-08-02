from flask import Flask
from routes.users import bp as users_bp
from routes.auth import bp as auth_bp

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
