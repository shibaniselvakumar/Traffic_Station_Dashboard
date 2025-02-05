
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import redis


db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*") 
redis_client = redis.StrictRedis.from_url("redis://localhost:6379/0", decode_responses=True)
