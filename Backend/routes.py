import time
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import redis
import threading
from .extensions import redis_client, socketio

# Blueprint for WebSocket events
from flask import Blueprint

events = Blueprint('events', __name__)

@socketio.on('connect')
def handle_connect():
    print("Dashboard connected to WebSocket!")

@socketio.on('disconnect')
def handle_disconnect():
    print("Dashboard disconnected from WebSocket!")

# Function to listen to Redis channel and emit events to WebSocket clients
def listen_to_redis():
    print("Starting Redis listener function...")

    while True:
        try:
            print("Checking Redis connection...")
            if redis_client.ping():
                print("✅ Redis is connected successfully!")
            else:
                print("❌ Redis ping failed!")
                time.sleep(5)
                continue  # Retry after 5 seconds
        except redis.exceptions.ConnectionError as e:
            print("❌ Redis connection error:", e)
            time.sleep(5)
            continue  # Retry after 5 seconds

        pubsub = redis_client.pubsub()
        pubsub.subscribe('ambulance_updates')
        print("📡 Subscribed to Redis channel: ambulance_updates")

        for message in pubsub.listen():
            print("📩 Raw message received from Redis:", message)  # Debug Redis message

            if message['type'] == 'message':
                try:
                    data = message['data']
                    print("🔄 Processing Redis message:", data)

                    order_id, latitude, longitude, timestamp, signal_id = data.split(",")
                    event_data = {
                        'order_id': order_id,
                        'latitude': latitude,
                        'longitude': longitude,
                        'timestamp': timestamp,
                        'signal_id': signal_id
                    }

                    print("✅ Processed update:", event_data)
                    with current_app.app_context():
                        socketio.emit('ambulance_signal_update', event_data)
                    print("📡 Event emitted to WebSocket clients.")

                except Exception as e:
                    print("❌ Error processing Redis message:", e)

# Start Redis listener in a separate thread so it doesn't block the main thread
def start_redis_listener():
    socketio.start_background_task(target=listen_to_redis)
