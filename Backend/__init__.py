from flask import Flask
import redis
from .routes import events, start_redis_listener
from .extensions import socketio

redis_client = redis.StrictRedis.from_url("redis://localhost:6379/0", decode_responses=True)

def create_app():
    app = Flask(__name__)
    app.config['REDIS_URL'] = "redis://localhost:6379/0"
    
    socketio.init_app(app)

    app.register_blueprint(events)

    start_redis_listener(app)

    return app
