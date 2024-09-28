from flask import Flask
from dotenv import load_dotenv
from routes import main as main_blueprint

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)  # Register your routes
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
