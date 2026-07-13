# app.py
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    version = os.getenv('APP_VERSION', 'v1.0')
    return f"""
    <html>
    <head><title>Flask ECS CI/CD Lab</title></head>
    <body>
        <h1>Flask ECS CI/CD Lab</h1>
        <p>Version: {version}</p>
        <p>Deployed via: {os.getenv('DEPLOY_METHOD', 'manual')}</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "version": os.getenv('APP_VERSION', 'v1.0')}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
