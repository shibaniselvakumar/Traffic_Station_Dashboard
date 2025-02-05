import threading
import time
from flask import Blueprint
import redis
from .extensions import redis_client, socketio 

# Blueprint for WebSocket events
events = Blueprint('events', __name__)

@socketio.on('connect')
def handle_connect():
    print("Dashboard connected to WebSocket!")

@socketio.on('disconnect')
def handle_disconnect():
    print("Dashboard disconnected from WebSocket!")

# Function to listen to Redis channel and emit events to WebSocket clients
def listen_to_redis():

        pubsub = redis_client.pubsub()
        pubsub.subscribe('ambulance_updates')
        print("Subscribed to Redis channel: ambulance_updates")

        for message in pubsub.listen():

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

                    print("Processed update:", event_data)
                    socketio.emit('ambulance_signal_update', event_data)
                    print("📡 Event emitted to WebSocket clients.")

                except Exception as e:
                    print("Error processing Redis message:", e)


def listen_for_crossed_signal():
    print("Listening for crossed signal updates...")

    while True:
        pubsub = redis_client.pubsub()
        pubsub.subscribe('signal_crossed_updates')  # New Redis channel for signal crossed updates
        print("📡 Subscribed to Redis channel: signal_crossed_updates")

        for message in pubsub.listen():
            print("📩 Raw message received from Redis:", message)

            if message['type'] == 'message':
                data = message['data']
                print("🔄 Processing Redis crossed signal message:", data)

                # Extract order_id and signal_id to remove corresponding log
                order_id, signal_id = data.split(",")
                crossed_data = {
                    'order_id': order_id,
                    'signal_id': signal_id
                }

                # Emit to frontend to remove the specific log
                socketio.emit('ambulance_signal_crossed', crossed_data)
                print("📡 Event emitted to WebSocket clients for crossed signal.")

# Start Redis listener in a separate thread so it doesn't block the main thread
def start_redis_listener():
    redis_thread = threading.Thread(target=listen_to_redis)
    redis_thread.daemon = True  # Allow thread to be killed when app exits
    redis_thread.start()

    signal_thread = threading.Thread(target=listen_for_crossed_signal)
    signal_thread.daemon = True  # Allow thread to be killed when app exits
    signal_thread.start()
