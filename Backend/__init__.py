from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import socketio
import redis

from .routes import events, start_redis_listener

db = SQLAlchemy()
redis_client = redis.StrictRedis.from_url("redis://localhost:6379/0", decode_responses=True)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/sample'
    app.config['REDIS_URL'] = "redis://localhost:6379/0"
    
    db.init_app(app)
    socketio.init_app(app)

    # Register events blueprint
    app.register_blueprint(events)

    # Start Redis listener in a background thread
    start_redis_listener()

    return app
