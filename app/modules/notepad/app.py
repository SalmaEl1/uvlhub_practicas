from flask import Flask
from app.routes import bp as tasks_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tasks_blueprint)
    return app
