from Backend import create_app
from Backend.extensions import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
