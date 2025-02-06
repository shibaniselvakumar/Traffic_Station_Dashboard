import threading
from flask import Blueprint
from .extensions import redis_client, socketio

events = Blueprint('events', __name__)

@socketio.on('connect')
def handle_connect():
    print("Dashboard connected to WebSocket!")

@socketio.on('disconnect')
def handle_disconnect():
    print("Dashboard disconnected from WebSocket!")

def listen_to_redis(app):
    with app.app_context():  # Explicitly using the app context
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

                    socketio.emit('ambulance_signal_update', event_data)
                    print("Event emitted to WebSocket clients.")

                except Exception as e:
                    print("Error processing Redis message:", e)

def listen_for_crossed_signal(app):
    with app.app_context():  # Explicitly using the app context
        pubsub = redis_client.pubsub()
        pubsub.subscribe('signal_crossed_updates')
        print("Subscribed to Redis channel: signal_crossed_updates")

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data']
                print("Processing Redis crossed signal message:", data)

                order_id, signal_id = data.split(",")
                crossed_data = {
                    'order_id': order_id,
                    'signal_id': signal_id
                }

                socketio.emit('ambulance_signal_crossed', crossed_data)
                print("Event emitted to WebSocket clients for crossed signal.")

def start_redis_listener(app):
    threading.Thread(target=listen_to_redis, args=(app,), daemon=True).start()
    threading.Thread(target=listen_for_crossed_signal, args=(app,), daemon=True).start()
