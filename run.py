import socketio
from Backend import create_app
from Backend.routes import start_redis_listener
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
    start_redis_listener()  # Start Redis listener before running the app
    socketio.run(app, debug=True) 
