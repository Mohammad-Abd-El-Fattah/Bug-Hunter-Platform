from flask import Flask
from .routes import init_routes
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  # Change to secure key
    init_db()  # Initialize the database
    init_routes(app)  # Register all routes
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

