import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_session import Session
from dotenv import load_dotenv


from routes.auth import auth_bp
from routes.trifecta import trifecta_bp
from routes.daily_challenges import daily_bp
from routes.progress import progress_bp

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
Session(app) 
socketio = SocketIO(app, cors_allowed_origins="*")


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(trifecta_bp, url_prefix='/trifecta')
app.register_blueprint(daily_bp, url_prefix='/daily')
app.register_blueprint(progress_bp, url_prefix='/progress')

@app.before_request
def log_request_info():
    logger.info(f"Handling request to {request.path} with method {request.method}")

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected via SocketIO')
    socketio.emit('message', {'data': 'Connected to server'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
